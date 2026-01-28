"""
Lead Scoring Service
====================

Calculates priority scores (0-100) using a weighted algorithm.

Formula:
    score = (value * 0.35) + (urgency * 0.25) + (tier * 0.20) +
            (budget * 0.15) + (strategic * 0.05)

Higher scores = higher priority in the queue.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Lead


class LeadScoringService:
    """Stateless scoring calculator."""

    # Weights (must sum to 1.0)
    WEIGHT_VALUE = 0.35
    WEIGHT_URGENCY = 0.25
    WEIGHT_TIER = 0.20
    WEIGHT_BUDGET = 0.15
    WEIGHT_STRATEGIC = 0.05

    # Value score thresholds
    VALUE_THRESHOLDS = [
        (100000, 100),
        (50000, 80),
        (20000, 60),
        (5000, 40),
        (0, 20),
    ]

    # Tier score mapping
    TIER_SCORES = {
        "strategic": 100,
        "existing": 70,
        "new": 40,
    }

    @classmethod
    def calculate_score(cls, lead: "Lead") -> int:
        """Calculate overall priority score for a lead."""
        value = cls._score_value(lead.estimated_value)
        urgency = cls._score_urgency(lead.urgency_level)
        tier = cls._score_tier(lead.client_tier)
        budget = 100 if lead.budget_confirmed else 0
        strategic = 100 if lead.strategic_fit else 0

        total = (
            (value * cls.WEIGHT_VALUE) +
            (urgency * cls.WEIGHT_URGENCY) +
            (tier * cls.WEIGHT_TIER) +
            (budget * cls.WEIGHT_BUDGET) +
            (strategic * cls.WEIGHT_STRATEGIC)
        )

        return max(0, min(100, round(total)))

    @classmethod
    def _score_value(cls, value: float) -> int:
        """Convert monetary value to score."""
        if not value:
            return 0
        for threshold, score in cls.VALUE_THRESHOLDS:
            if value >= threshold:
                return score
        return 0

    @classmethod
    def _score_urgency(cls, level: int) -> int:
        """Convert urgency level (1-5) to score."""
        if not level:
            return 60
        return max(1, min(5, level)) * 20

    @classmethod
    def _score_tier(cls, tier: str) -> int:
        """Convert client tier to score."""
        return cls.TIER_SCORES.get(tier, 40)

    @classmethod
    def get_breakdown(cls, lead: "Lead") -> dict:
        """Get detailed score breakdown for debugging."""
        return {
            "value": {"score": cls._score_value(lead.estimated_value), "weight": cls.WEIGHT_VALUE},
            "urgency": {"score": cls._score_urgency(lead.urgency_level), "weight": cls.WEIGHT_URGENCY},
            "tier": {"score": cls._score_tier(lead.client_tier), "weight": cls.WEIGHT_TIER},
            "budget": {"score": 100 if lead.budget_confirmed else 0, "weight": cls.WEIGHT_BUDGET},
            "strategic": {"score": 100 if lead.strategic_fit else 0, "weight": cls.WEIGHT_STRATEGIC},
            "total": cls.calculate_score(lead)
        }
