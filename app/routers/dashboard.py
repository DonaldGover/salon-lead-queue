"""
Dashboard Endpoints
===================

HTML frontend using HTMX and Jinja2 templates.
"""
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.prioritization import QueueManager
from app import crud

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


@router.get("/catalog", response_class=HTMLResponse)
def catalog(
    request: Request,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Service catalog dashboard."""
    categories = crud.get_categories(db)
    services_by_category = crud.get_services_by_category(db)
    catalog_stats = crud.get_catalog_stats(db)

    # Filter by category if specified
    filtered_services = None
    active_category = None
    if category:
        cat = crud.get_category_by_slug(db, category)
        if cat:
            active_category = cat.to_dict()
            filtered_services = crud.get_services(db, category_id=cat.id)

    return templates.TemplateResponse("catalog.html", {
        "request": request,
        "categories": categories,
        "services_by_category": services_by_category,
        "catalog_stats": catalog_stats,
        "filtered_services": filtered_services,
        "active_category": active_category,
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


@router.get("/partials/catalog-services", response_class=HTMLResponse)
def catalog_services_partial(
    request: Request,
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """HTMX partial: catalog services list."""
    services = []
    category_info = None

    if category:
        cat = crud.get_category_by_slug(db, category)
        if cat:
            category_info = cat.to_dict()
            services = crud.get_services(db, category_id=cat.id)
    else:
        services = crud.get_services(db)

    return templates.TemplateResponse("partials/catalog_services.html", {
        "request": request,
        "services": services,
        "category": category_info,
    })
