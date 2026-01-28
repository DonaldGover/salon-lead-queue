"""
CRUD Operations
===============

Database access layer for lead management.
All database reads/writes go through these functions.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List

from app.models import Lead, LeadActivity
from app.schemas import LeadCreate, LeadUpdate
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
