"""
Services Router
===============

API endpoints for managing the salon service catalog.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import crud
from app.schemas import (
    ServiceCreate, ServiceUpdate, ServiceResponse, ServiceListResponse,
    CategoryCreate, CategoryResponse, CatalogStats, MessageResponse
)

router = APIRouter(prefix="/services", tags=["services"])


# =============================================================================
# CATEGORY ENDPOINTS
# =============================================================================

@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Get all service categories."""
    return crud.get_categories(db)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    existing = crud.get_category_by_slug(db, data.slug)
    if existing:
        raise HTTPException(status_code=400, detail=f"Category with slug '{data.slug}' already exists")
    return crud.create_category(db, data)


@router.get("/categories/{slug}", response_model=CategoryResponse)
def get_category(slug: str, db: Session = Depends(get_db)):
    """Get a category by slug."""
    category = crud.get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# =============================================================================
# SERVICE ENDPOINTS
# =============================================================================

@router.get("", response_model=ServiceListResponse)
def list_services(
    category: Optional[str] = Query(None, description="Filter by category slug"),
    active_only: bool = Query(True, description="Only return active services"),
    bookable_only: bool = Query(False, description="Only return bookable services"),
    search: Optional[str] = Query(None, description="Search by service name"),
    group_by_category: bool = Query(False, description="Group results by category"),
    db: Session = Depends(get_db)
):
    """List all services with optional filtering."""
    category_id = None
    if category:
        cat = crud.get_category_by_slug(db, category)
        if cat:
            category_id = cat.id

    services = crud.get_services(
        db,
        category_id=category_id,
        active_only=active_only,
        bookable_only=bookable_only,
        search=search
    )

    by_category = None
    if group_by_category:
        by_category = crud.get_services_by_category(db, active_only=active_only)

    return ServiceListResponse(
        services=[ServiceResponse(**s.to_dict()) for s in services],
        total=len(services),
        by_category=by_category
    )


@router.post("", response_model=ServiceResponse, status_code=201)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    """Create a new service."""
    category = crud.get_category(db, data.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    return ServiceResponse(**crud.create_service(db, data).to_dict())


@router.get("/stats", response_model=CatalogStats)
def get_catalog_stats(db: Session = Depends(get_db)):
    """Get catalog statistics."""
    return crud.get_catalog_stats(db)


@router.post("/seed", response_model=MessageResponse)
def seed_catalog(db: Session = Depends(get_db)):
    """Seed the catalog with default data from screenshots."""
    stats = crud.seed_catalog(db)
    return MessageResponse(
        message=f"Seeded {stats['categories_created']} categories and {stats['services_created']} services ({stats['skipped']} skipped)",
        success=True
    )


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: str, db: Session = Depends(get_db)):
    """Get a single service by ID."""
    service = crud.get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return ServiceResponse(**service.to_dict())


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: str, data: ServiceUpdate, db: Session = Depends(get_db)):
    """Update a service."""
    service = crud.update_service(db, service_id, data)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return ServiceResponse(**service.to_dict())


@router.delete("/{service_id}", response_model=MessageResponse)
def delete_service(
    service_id: str,
    hard: bool = Query(False, description="Permanently delete instead of deactivating"),
    db: Session = Depends(get_db)
):
    """Delete or deactivate a service."""
    success = crud.delete_service(db, service_id, hard=hard)
    if not success:
        raise HTTPException(status_code=404, detail="Service not found")

    action = "deleted" if hard else "deactivated"
    return MessageResponse(message=f"Service {action} successfully")
