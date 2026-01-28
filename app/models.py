"""
Database Models
===============

SQLAlchemy ORM models defining the database schema.

Tables:
    - leads: Core lead data with scoring attributes
    - lead_activities: Audit trail for all changes
"""
from sqlalchemy import (
    Column, String, Text, Float, Integer, Boolean,
    DateTime, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


def generate_uuid() -> str:
    """Generate UUID string for primary keys."""
    return str(uuid.uuid4())


class Lead(Base):
    """
    Lead model - represents a potential client in the queue.

    Scoring is calculated from:
        - estimated_value: Project monetary value
        - urgency_level: Time sensitivity (1-5)
        - client_tier: Relationship status
        - budget_confirmed: Has allocated funds
        - strategic_fit: Aligns with goals
    """
    __tablename__ = "leads"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    # Contact
    company_name = Column(String(255), nullable=False, index=True)
    contact_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))

    # Project
    project_description = Column(Text)
    source = Column(String(100))

    # Scoring factors
    estimated_value = Column(Float, default=0.0)
    urgency_level = Column(Integer, default=3)
    client_tier = Column(String(20), default="new")
    budget_confirmed = Column(Boolean, default=False)
    strategic_fit = Column(Boolean, default=False)

    # Calculated
    score = Column(Integer, default=0, index=True)
    queue_position = Column(Integer, default=999, index=True)

    # Status
    status = Column(String(20), default="new", index=True)
    assigned_to = Column(String(100))

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Soft delete
    is_active = Column(Boolean, default=True, index=True)

    # Relations
    activities = relationship("LeadActivity", back_populates="lead", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("urgency_level >= 1 AND urgency_level <= 5", name="ck_urgency"),
        CheckConstraint("client_tier IN ('new', 'existing', 'strategic')", name="ck_tier"),
        CheckConstraint("status IN ('new', 'contacted', 'qualified', 'proposal', 'won', 'lost')", name="ck_status"),
    )

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "email": self.email,
            "phone": self.phone,
            "project_description": self.project_description,
            "source": self.source,
            "estimated_value": self.estimated_value,
            "urgency_level": self.urgency_level,
            "client_tier": self.client_tier,
            "budget_confirmed": self.budget_confirmed,
            "strategic_fit": self.strategic_fit,
            "score": self.score,
            "queue_position": self.queue_position,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }


class LeadActivity(Base):
    """
    Activity log - audit trail for lead changes.

    Records both manual activities (calls, notes) and
    system-generated changes (field updates).
    """
    __tablename__ = "lead_activities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    lead_id = Column(String(36), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)

    activity_type = Column(String(50), nullable=False)
    description = Column(Text)

    # Change tracking
    field_changed = Column(String(100))
    old_value = Column(Text)
    new_value = Column(Text)

    performed_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    lead = relationship("Lead", back_populates="activities")

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "activity_type": self.activity_type,
            "description": self.description,
            "field_changed": self.field_changed,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "performed_by": self.performed_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
