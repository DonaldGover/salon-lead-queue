"""
Lead CRUD Endpoints
===================

RESTful API for lead management.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import math

from app.database import get_db
from app import crud
from app.schemas import (
    LeadCreate, LeadUpdate, LeadResponse, LeadListResponse,
    ActivityCreate, ActivityResponse, MessageResponse
)

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("", response_model=LeadResponse, status_code=201)
def create_lead(data: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead."""
    return crud.create_lead(db, data)


@router.get("", response_model=LeadListResponse)
def list_leads(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    client_tier: Optional[str] = None,
    is_active: bool = True,
    order_by: str = "queue_position",
    db: Session = Depends(get_db)
):
    """List leads with pagination."""
    skip = (page - 1) * page_size
    leads = crud.get_leads(db, skip, page_size, status, client_tier, is_active, order_by)
    total = crud.get_leads_count(db, status, client_tier, is_active)

    return {
        "leads": leads,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total > 0 else 1
    }


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: str, db: Session = Depends(get_db)):
    """Get a single lead."""
    lead = crud.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    return lead


@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: str, data: LeadUpdate, db: Session = Depends(get_db)):
    """Update a lead."""
    lead = crud.update_lead(db, lead_id, data)
    if not lead:
        raise HTTPException(404, "Lead not found")
    return lead


@router.delete("/{lead_id}", response_model=MessageResponse)
def delete_lead(lead_id: str, db: Session = Depends(get_db)):
    """Soft delete a lead."""
    if not crud.delete_lead(db, lead_id):
        raise HTTPException(404, "Lead not found")
    return {"message": "Lead deleted", "success": True}


@router.put("/{lead_id}/reorder", response_model=LeadResponse)
def reorder_lead(lead_id: str, position: int = Query(..., ge=0), db: Session = Depends(get_db)):
    """Move lead to specific queue position."""
    lead = crud.update_lead_position(db, lead_id, position)
    if not lead:
        raise HTTPException(404, "Lead not found")
    return lead


@router.get("/{lead_id}/activities", response_model=list[ActivityResponse])
def get_activities(lead_id: str, limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    """Get activity history for a lead."""
    if not crud.get_lead(db, lead_id):
        raise HTTPException(404, "Lead not found")
    return crud.get_lead_activities(db, lead_id, limit)


@router.post("/{lead_id}/activities", response_model=ActivityResponse, status_code=201)
def create_activity(lead_id: str, data: ActivityCreate, db: Session = Depends(get_db)):
    """Log an activity on a lead."""
    if not crud.get_lead(db, lead_id):
        raise HTTPException(404, "Lead not found")
    return crud.log_activity(db, lead_id, data.activity_type, data.description, performed_by=data.performed_by)
