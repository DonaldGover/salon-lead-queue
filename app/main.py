"""
FastAPI Application
===================

Main entry point for the Salon Lead Queue API.
"""
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.routers import health, leads, queue, dashboard, services


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    print("[Salon] Starting up...")
    init_db()
    print("[Salon] Database initialized")
    yield
    print("[Salon] Shutting down...")


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title="Salon Lead Queue",
        description="Business lead management and prioritization API",
        version="1.0.0",
        lifespan=lifespan
    )

    # Templates
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    (templates_dir / "partials").mkdir(exist_ok=True)

    templates = Jinja2Templates(directory=str(templates_dir))
    dashboard.set_templates(templates)

    # Routes
    app.include_router(health.router)
    app.include_router(leads.router)
    app.include_router(queue.router)
    app.include_router(services.router)
    app.include_router(dashboard.router)

    return app


app = create_app()


if __name__ == "__main__":
    import os
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
