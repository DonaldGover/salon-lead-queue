"""
Pydantic Schemas
================

Request/response validation models for the API.
Ensures data integrity and generates OpenAPI documentation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class LeadCreate(BaseModel):
    """Input schema for creating a lead."""
    company_name: str = Field(..., min_length=1, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    project_description: Optional[str] = None
    source: Optional[str] = Field(None, max_length=100)
    estimated_value: float = Field(default=0.0, ge=0)
    urgency_level: int = Field(default=3, ge=1, le=5)
    client_tier: Literal["new", "existing", "strategic"] = "new"
    budget_confirmed: bool = False
    strategic_fit: bool = False
    assigned_to: Optional[str] = Field(None, max_length=100)


class LeadUpdate(BaseModel):
    """Input schema for updating a lead (all fields optional)."""
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    project_description: Optional[str] = None
    source: Optional[str] = Field(None, max_length=100)
    estimated_value: Optional[float] = Field(None, ge=0)
    urgency_level: Optional[int] = Field(None, ge=1, le=5)
    client_tier: Optional[Literal["new", "existing", "strategic"]] = None
    budget_confirmed: Optional[bool] = None
    strategic_fit: Optional[bool] = None
    status: Optional[Literal["new", "contacted", "qualified", "proposal", "won", "lost"]] = None
    assigned_to: Optional[str] = Field(None, max_length=100)
    queue_position: Optional[int] = Field(None, ge=0)


class LeadResponse(BaseModel):
    """Output schema for lead data."""
    id: str
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    project_description: Optional[str] = None
    source: Optional[str] = None
    estimated_value: float
    urgency_level: int
    client_tier: str
    budget_confirmed: bool
    strategic_fit: bool
    score: int
    queue_position: int
    status: str
    assigned_to: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Paginated list of leads."""
    leads: List[LeadResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class QueueStats(BaseModel):
    """Queue metrics for dashboard."""
    total_leads: int
    active_leads: int
    by_status: dict
    by_tier: dict
    total_value: float
    avg_score: float
    high_priority_count: int


class BulkReorderRequest(BaseModel):
    """Bulk reorder multiple leads."""
    lead_positions: List[dict]


class ActivityCreate(BaseModel):
    """Input schema for logging an activity."""
    activity_type: Literal["note", "call", "email", "meeting", "other"]
    description: Optional[str] = None
    performed_by: Optional[str] = None


class ActivityResponse(BaseModel):
    """Output schema for activity data."""
    id: str
    lead_id: str
    activity_type: str
    description: Optional[str] = None
    field_changed: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    performed_by: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic success message."""
    message: str
    success: bool = True


# =============================================================================
# SERVICE CATALOG SCHEMAS
# =============================================================================

CATEGORY_SLUGS = Literal[
    "hair", "lashes_brows", "waxing", "nails",
    "massage_body", "skincare_facials", "makeup", "consultation_admin"
]


class CategoryCreate(BaseModel):
    """Input schema for creating a category."""
    slug: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-z_]+$")
    name: str = Field(..., min_length=1, max_length=100)
    sort_order: int = Field(default=0, ge=0)
    is_bookable_default: bool = True
    color_tag: str = Field(default="#6366f1", pattern=r"^#[0-9a-fA-F]{6}$")


class CategoryResponse(BaseModel):
    """Output schema for category data."""
    id: str
    slug: str
    name: str
    sort_order: int
    is_bookable_default: bool
    color_tag: str

    class Config:
        from_attributes = True


class ServiceCreate(BaseModel):
    """Input schema for creating a service."""
    category_id: str
    name: str = Field(..., min_length=1, max_length=200)
    default_duration_min: int = Field(..., ge=0, le=480)
    default_price_usd: float = Field(..., ge=0)
    bookable: bool = True
    active: bool = True
    tags: Optional[str] = None
    notes: Optional[str] = None


class ServiceUpdate(BaseModel):
    """Input schema for updating a service."""
    category_id: Optional[str] = None
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    default_duration_min: Optional[int] = Field(None, ge=0, le=480)
    default_price_usd: Optional[float] = Field(None, ge=0)
    bookable: Optional[bool] = None
    active: Optional[bool] = None
    tags: Optional[str] = None
    notes: Optional[str] = None


class ServiceResponse(BaseModel):
    """Output schema for service data."""
    id: str
    category_id: str
    category_slug: Optional[str] = None
    category_name: Optional[str] = None
    name: str
    default_duration_min: int
    default_price_usd: float
    bookable: bool
    active: bool
    tags: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ServiceListResponse(BaseModel):
    """List of services with optional category grouping."""
    services: List[ServiceResponse]
    total: int
    by_category: Optional[dict] = None


class StylistSettingCreate(BaseModel):
    """Input schema for stylist service override."""
    stylist_id: str
    service_id: str
    enabled: bool = True
    custom_price_usd: Optional[float] = Field(None, ge=0)


class StylistSettingResponse(BaseModel):
    """Output schema for stylist service setting."""
    id: str
    stylist_id: str
    service_id: str
    enabled: bool
    custom_price_usd: Optional[float] = None
    effective_price: Optional[float] = None

    class Config:
        from_attributes = True


class CatalogStats(BaseModel):
    """Service catalog statistics."""
    total_services: int
    active_services: int
    bookable_services: int
    by_category: dict
    price_range: dict
    duration_range: dict
