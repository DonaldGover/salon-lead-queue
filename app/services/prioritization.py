"""
Queue Prioritization Service
============================

Manages lead ordering in the priority queue.

Supports:
    - Auto-sort by score
    - Manual reordering
    - Queue statistics
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict

from app.models import Lead
from app.services.scoring import LeadScoringService


class QueueManager:
    """Queue management operations."""

    @staticmethod
    def auto_prioritize(db: Session) -> int:
        """Sort queue by score (highest first)."""
        leads = db.query(Lead).filter(
            Lead.is_active == True
        ).order_by(desc(Lead.score), Lead.created_at).all()

        for i, lead in enumerate(leads):
            lead.queue_position = i

        db.commit()
        return len(leads)

    @staticmethod
    def recalculate_all_scores(db: Session) -> int:
        """Recalculate scores for all active leads."""
        leads = db.query(Lead).filter(Lead.is_active == True).all()

        for lead in leads:
            lead.score = LeadScoringService.calculate_score(lead)

        db.commit()
        return len(leads)

    @staticmethod
    def move_lead(db: Session, lead_id: str, new_position: int) -> bool:
        """Move a lead to a specific position."""
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return False

        old = lead.queue_position
        if old == new_position:
            return True

        if new_position < old:
            db.query(Lead).filter(
                Lead.queue_position >= new_position,
                Lead.queue_position < old,
                Lead.is_active == True,
                Lead.id != lead_id
            ).update({Lead.queue_position: Lead.queue_position + 1}, synchronize_session=False)
        else:
            db.query(Lead).filter(
                Lead.queue_position <= new_position,
                Lead.queue_position > old,
                Lead.is_active == True,
                Lead.id != lead_id
            ).update({Lead.queue_position: Lead.queue_position - 1}, synchronize_session=False)

        lead.queue_position = new_position
        db.commit()
        return True

    @staticmethod
    def bulk_reorder(db: Session, positions: List[Dict]) -> int:
        """Set positions for multiple leads."""
        count = 0
        for item in positions:
            lead = db.query(Lead).filter(Lead.id == item["lead_id"]).first()
            if lead:
                lead.queue_position = item["position"]
                count += 1
        db.commit()
        return count

    @staticmethod
    def get_queue(db: Session, limit: int = 50) -> List[Lead]:
        """Get prioritized queue of active leads."""
        return db.query(Lead).filter(
            Lead.is_active == True
        ).order_by(Lead.queue_position).limit(limit).all()

    @staticmethod
    def get_stats(db: Session) -> Dict:
        """Calculate queue statistics."""
        total = db.query(func.count(Lead.id)).scalar() or 0
        active = db.query(func.count(Lead.id)).filter(Lead.is_active == True).scalar() or 0

        status_counts = db.query(Lead.status, func.count(Lead.id)).filter(
            Lead.is_active == True
        ).group_by(Lead.status).all()
        by_status = {s: c for s, c in status_counts}

        tier_counts = db.query(Lead.client_tier, func.count(Lead.id)).filter(
            Lead.is_active == True
        ).group_by(Lead.client_tier).all()
        by_tier = {t: c for t, c in tier_counts}

        total_value = db.query(func.sum(Lead.estimated_value)).filter(Lead.is_active == True).scalar() or 0.0
        avg_score = db.query(func.avg(Lead.score)).filter(Lead.is_active == True).scalar() or 0.0
        high_priority = db.query(func.count(Lead.id)).filter(Lead.is_active == True, Lead.score >= 70).scalar() or 0

        return {
            "total_leads": total,
            "active_leads": active,
            "by_status": by_status,
            "by_tier": by_tier,
            "total_value": float(total_value),
            "avg_score": round(float(avg_score), 1),
            "high_priority_count": high_priority
        }

    @staticmethod
    def normalize_positions(db: Session) -> int:
        """Fix gaps in queue positions."""
        leads = db.query(Lead).filter(Lead.is_active == True).order_by(Lead.queue_position).all()
        for i, lead in enumerate(leads):
            lead.queue_position = i
        db.commit()
        return len(leads)
