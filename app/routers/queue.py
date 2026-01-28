"""
Queue Management Endpoints
==========================

Priority queue operations and statistics.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import LeadResponse, QueueStats, BulkReorderRequest, MessageResponse
from app.services.prioritization import QueueManager

router = APIRouter(prefix="/queue", tags=["Queue"])


@router.get("", response_model=List[LeadResponse])
def get_queue(limit: int = 50, db: Session = Depends(get_db)):
    """Get prioritized lead queue."""
    return QueueManager.get_queue(db, limit)


@router.post("/reprioritize", response_model=MessageResponse)
def reprioritize(db: Session = Depends(get_db)):
    """Auto-sort queue by score."""
    count = QueueManager.auto_prioritize(db)
    return {"message": f"Reprioritized {count} leads", "success": True}


@router.get("/stats", response_model=QueueStats)
def get_stats(db: Session = Depends(get_db)):
    """Get queue statistics."""
    return QueueManager.get_stats(db)


@router.post("/reorder", response_model=MessageResponse)
def bulk_reorder(request: BulkReorderRequest, db: Session = Depends(get_db)):
    """Bulk reorder multiple leads."""
    count = QueueManager.bulk_reorder(db, request.lead_positions)
    return {"message": f"Reordered {count} leads", "success": True}


@router.post("/recalculate", response_model=MessageResponse)
def recalculate(db: Session = Depends(get_db)):
    """Recalculate all lead scores."""
    count = QueueManager.recalculate_all_scores(db)
    return {"message": f"Recalculated {count} scores", "success": True}


@router.post("/normalize", response_model=MessageResponse)
def normalize(db: Session = Depends(get_db)):
    """Fix gaps in queue positions."""
    count = QueueManager.normalize_positions(db)
    return {"message": f"Normalized {count} positions", "success": True}
