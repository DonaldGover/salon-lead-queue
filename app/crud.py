"""
CRUD Operations
===============

Database access layer for lead management and service catalog.
All database reads/writes go through these functions.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List

from app.models import Lead, LeadActivity, MasterCategory, MasterService, StylistServiceSetting
from app.schemas import LeadCreate, LeadUpdate, ServiceCreate, ServiceUpdate, CategoryCreate
from app.services.scoring import LeadScoringService


def create_lead(db: Session, data: LeadCreate, performed_by: str = None) -> Lead:
    """Create a new lead with auto-calculated score."""
    lead = Lead(**data.model_dump())
    lead.score = LeadScoringService.calculate_score(lead)

    max_pos = db.query(func.max(Lead.queue_position)).scalar() or 0
    lead.queue_position = max_pos + 1

    db.add(lead)
    db.commit()
    db.refresh(lead)

    log_activity(db, lead.id, "created", f"Lead created: {lead.company_name}", performed_by=performed_by)
    return lead


def get_lead(db: Session, lead_id: str) -> Optional[Lead]:
    """Get a single lead by ID."""
    return db.query(Lead).filter(Lead.id == lead_id).first()


def get_leads(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    client_tier: str = None,
    is_active: bool = True,
    order_by: str = "queue_position"
) -> List[Lead]:
    """List leads with filtering and pagination."""
    query = db.query(Lead)

    if is_active is not None:
        query = query.filter(Lead.is_active == is_active)
    if status:
        query = query.filter(Lead.status == status)
    if client_tier:
        query = query.filter(Lead.client_tier == client_tier)

    if order_by == "score":
        query = query.order_by(desc(Lead.score))
    elif order_by == "created_at":
        query = query.order_by(desc(Lead.created_at))
    else:
        query = query.order_by(Lead.queue_position)

    return query.offset(skip).limit(limit).all()


def get_leads_count(db: Session, status: str = None, client_tier: str = None, is_active: bool = True) -> int:
    """Count leads matching filters."""
    query = db.query(func.count(Lead.id))
    if is_active is not None:
        query = query.filter(Lead.is_active == is_active)
    if status:
        query = query.filter(Lead.status == status)
    if client_tier:
        query = query.filter(Lead.client_tier == client_tier)
    return query.scalar()


def update_lead(db: Session, lead_id: str, data: LeadUpdate, performed_by: str = None) -> Optional[Lead]:
    """Update a lead's fields."""
    lead = get_lead(db, lead_id)
    if not lead:
        return None

    update_data = data.model_dump(exclude_unset=True)
    scoring_fields = {'estimated_value', 'urgency_level', 'client_tier', 'budget_confirmed', 'strategic_fit'}
    score_changed = False

    for field, new_value in update_data.items():
        old_value = getattr(lead, field)
        if old_value == new_value:
            continue

        setattr(lead, field, new_value)

        if field in scoring_fields:
            score_changed = True

        log_activity(db, lead_id, "updated", f"Changed {field}",
                     field_changed=field,
                     old_value=str(old_value) if old_value is not None else None,
                     new_value=str(new_value) if new_value is not None else None,
                     performed_by=performed_by)

    if score_changed:
        lead.score = LeadScoringService.calculate_score(lead)

    db.commit()
    db.refresh(lead)
    return lead


def update_lead_position(db: Session, lead_id: str, new_position: int) -> Optional[Lead]:
    """Move a lead to a specific queue position."""
    lead = get_lead(db, lead_id)
    if not lead:
        return None

    old_position = lead.queue_position
    if old_position == new_position:
        return lead

    if new_position < old_position:
        db.query(Lead).filter(
            Lead.queue_position >= new_position,
            Lead.queue_position < old_position,
            Lead.id != lead_id
        ).update({Lead.queue_position: Lead.queue_position + 1})
    else:
        db.query(Lead).filter(
            Lead.queue_position <= new_position,
            Lead.queue_position > old_position,
            Lead.id != lead_id
        ).update({Lead.queue_position: Lead.queue_position - 1})

    lead.queue_position = new_position
    db.commit()
    db.refresh(lead)
    return lead


def delete_lead(db: Session, lead_id: str, performed_by: str = None) -> bool:
    """Soft delete a lead."""
    lead = get_lead(db, lead_id)
    if not lead:
        return False

    lead.is_active = False
    log_activity(db, lead_id, "deleted", "Lead soft deleted", performed_by=performed_by)
    db.commit()
    return True


def log_activity(
    db: Session,
    lead_id: str,
    activity_type: str,
    description: str = None,
    field_changed: str = None,
    old_value: str = None,
    new_value: str = None,
    performed_by: str = None
) -> LeadActivity:
    """Record an activity in the audit log."""
    activity = LeadActivity(
        lead_id=lead_id,
        activity_type=activity_type,
        description=description,
        field_changed=field_changed,
        old_value=old_value,
        new_value=new_value,
        performed_by=performed_by
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def get_lead_activities(db: Session, lead_id: str, limit: int = 50) -> List[LeadActivity]:
    """Get activity history for a lead."""
    return db.query(LeadActivity).filter(
        LeadActivity.lead_id == lead_id
    ).order_by(desc(LeadActivity.created_at)).limit(limit).all()


# =============================================================================
# SERVICE CATALOG CRUD
# =============================================================================

def create_category(db: Session, data: CategoryCreate) -> MasterCategory:
    """Create a new service category."""
    category = MasterCategory(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category(db: Session, category_id: str) -> Optional[MasterCategory]:
    """Get category by ID."""
    return db.query(MasterCategory).filter(MasterCategory.id == category_id).first()


def get_category_by_slug(db: Session, slug: str) -> Optional[MasterCategory]:
    """Get category by slug."""
    return db.query(MasterCategory).filter(MasterCategory.slug == slug).first()


def get_categories(db: Session) -> List[MasterCategory]:
    """Get all categories ordered by sort_order."""
    return db.query(MasterCategory).order_by(MasterCategory.sort_order).all()


def create_service(db: Session, data: ServiceCreate) -> MasterService:
    """Create a new master service."""
    service = MasterService(**data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_service(db: Session, service_id: str) -> Optional[MasterService]:
    """Get service by ID."""
    return db.query(MasterService).filter(MasterService.id == service_id).first()


def get_services(
    db: Session,
    category_id: str = None,
    active_only: bool = True,
    bookable_only: bool = False,
    search: str = None
) -> List[MasterService]:
    """List services with filtering."""
    query = db.query(MasterService)

    if active_only:
        query = query.filter(MasterService.active == True)
    if bookable_only:
        query = query.filter(MasterService.bookable == True)
    if category_id:
        query = query.filter(MasterService.category_id == category_id)
    if search:
        query = query.filter(MasterService.name.ilike(f"%{search}%"))

    return query.order_by(MasterService.name).all()


def get_services_by_category(db: Session, active_only: bool = True) -> dict:
    """Get all services grouped by category."""
    categories = get_categories(db)
    result = {}

    for cat in categories:
        services = get_services(db, category_id=cat.id, active_only=active_only)
        result[cat.slug] = {
            "category": cat.to_dict(),
            "services": [s.to_dict() for s in services],
            "count": len(services)
        }

    return result


def update_service(db: Session, service_id: str, data: ServiceUpdate) -> Optional[MasterService]:
    """Update a service's fields."""
    service = get_service(db, service_id)
    if not service:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: str, hard: bool = False) -> bool:
    """Delete or deactivate a service."""
    service = get_service(db, service_id)
    if not service:
        return False

    if hard:
        db.delete(service)
    else:
        service.active = False

    db.commit()
    return True


def get_services_count(db: Session, active_only: bool = True, bookable_only: bool = False) -> int:
    """Count services matching filters."""
    query = db.query(func.count(MasterService.id))
    if active_only:
        query = query.filter(MasterService.active == True)
    if bookable_only:
        query = query.filter(MasterService.bookable == True)
    return query.scalar()


def get_catalog_stats(db: Session) -> dict:
    """Get catalog statistics."""
    total = db.query(func.count(MasterService.id)).scalar() or 0
    active = db.query(func.count(MasterService.id)).filter(MasterService.active == True).scalar() or 0
    bookable = db.query(func.count(MasterService.id)).filter(
        MasterService.active == True, MasterService.bookable == True
    ).scalar() or 0

    price_min = db.query(func.min(MasterService.default_price_usd)).filter(MasterService.active == True).scalar() or 0
    price_max = db.query(func.max(MasterService.default_price_usd)).filter(MasterService.active == True).scalar() or 0
    price_avg = db.query(func.avg(MasterService.default_price_usd)).filter(MasterService.active == True).scalar() or 0

    dur_min = db.query(func.min(MasterService.default_duration_min)).filter(
        MasterService.active == True, MasterService.default_duration_min > 0
    ).scalar() or 0
    dur_max = db.query(func.max(MasterService.default_duration_min)).filter(MasterService.active == True).scalar() or 0
    dur_avg = db.query(func.avg(MasterService.default_duration_min)).filter(
        MasterService.active == True, MasterService.default_duration_min > 0
    ).scalar() or 0

    by_category = {}
    for cat in get_categories(db):
        count = db.query(func.count(MasterService.id)).filter(
            MasterService.category_id == cat.id, MasterService.active == True
        ).scalar() or 0
        by_category[cat.slug] = count

    return {
        "total_services": total,
        "active_services": active,
        "bookable_services": bookable,
        "by_category": by_category,
        "price_range": {"min": price_min, "max": price_max, "avg": round(price_avg, 2)},
        "duration_range": {"min": dur_min, "max": dur_max, "avg": round(dur_avg, 2)},
    }


# =============================================================================
# CATALOG SEEDING
# =============================================================================

def seed_catalog(db: Session) -> dict:
    """Seed the database with catalog data from screenshots."""
    from app.data.catalog import CATEGORIES, SERVICES

    stats = {"categories_created": 0, "services_created": 0, "skipped": 0}

    # Seed categories
    for cat_data in CATEGORIES:
        existing = get_category_by_slug(db, cat_data["slug"])
        if existing:
            stats["skipped"] += 1
            continue

        category = MasterCategory(
            slug=cat_data["slug"],
            name=cat_data["name"],
            sort_order=cat_data.get("sort_order", 0),
            is_bookable_default=cat_data.get("is_bookable_default", True),
            color_tag=cat_data.get("color_tag", "#6366f1")
        )
        db.add(category)
        stats["categories_created"] += 1

    db.commit()

    # Seed services
    for category_slug, services in SERVICES.items():
        category = get_category_by_slug(db, category_slug)
        if not category:
            continue

        for name, duration, price, tags in services:
            # Check if service already exists
            existing = db.query(MasterService).filter(
                MasterService.category_id == category.id,
                MasterService.name == name
            ).first()

            if existing:
                stats["skipped"] += 1
                continue

            bookable = True
            if tags:
                if any(t in tags for t in ["consultation", "fee", "deposit"]):
                    bookable = False

            service = MasterService(
                category_id=category.id,
                name=name,
                default_duration_min=duration,
                default_price_usd=price,
                tags=tags,
                bookable=bookable,
                active=True
            )
            db.add(service)
            stats["services_created"] += 1

    db.commit()
    return stats
