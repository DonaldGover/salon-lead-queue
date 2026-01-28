"""
Dashboard Endpoints
===================

HTML frontend using HTMX and Jinja2 templates.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.prioritization import QueueManager

router = APIRouter(tags=["Dashboard"])

# Set by main.py after template configuration
templates = None


def set_templates(t):
    """Configure Jinja2 templates instance."""
    global templates
    templates = t


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Main dashboard page."""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": QueueManager.get_stats(db),
        "queue": QueueManager.get_queue(db, 50)
    })


@router.get("/partials/queue", response_class=HTMLResponse)
def queue_partial(request: Request, db: Session = Depends(get_db)):
    """HTMX partial: queue list."""
    return templates.TemplateResponse("partials/queue_list.html", {
        "request": request,
        "queue": QueueManager.get_queue(db, 50)
    })


@router.get("/partials/stats", response_class=HTMLResponse)
def stats_partial(request: Request, db: Session = Depends(get_db)):
    """HTMX partial: stats panel."""
    return templates.TemplateResponse("partials/stats_panel.html", {
        "request": request,
        "stats": QueueManager.get_stats(db)
    })
