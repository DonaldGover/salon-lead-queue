"""
Health Check Endpoints
======================

System monitoring and status endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db

router = APIRouter(tags=["Health"])


@router.get("/")
def root():
    """API status check."""
    return {"status": "online", "service": "Salon Lead Queue", "version": "1.0.0"}


@router.get("/health")
def health(db: Session = Depends(get_db)):
    """Detailed health check including database."""
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status
    }
