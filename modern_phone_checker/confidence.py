"""Confidence scoring system for verifications.

This module implements a scoring system that considers multiple
factors to assess the reliability of a verification.
"""

from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class PlatformReliability:
    """Reliability configuration for a platform.

    Attributes:
        base_score: Base score for the platform (0.0 to 1.0)
        api_timeouts: Number of recent timeouts
        success_rate: Success rate of recent verifications
        last_failure: Timestamp of last failure
    """

    base_score: float = 0.8
    api_timeouts: int = 0
    success_rate: float = 1.0
    last_failure: Optional[datetime] = None


class ConfidenceScorer:
    """Confidence score calculator for verifications."""

    def __init__(self):
        # Base scores for each platform based on historical reliability
        self.platform_scores: Dict[str, PlatformReliability] = {
            "whatsapp": PlatformReliability(base_score=0.9),
            "telegram": PlatformReliability(base_score=0.85),
            "instagram": PlatformReliability(base_score=0.75),
            "snapchat": PlatformReliability(base_score=0.7),
        }

        # Weight factors for score components
        self.weights: Dict[str, float] = {
            "platform_reliability": 0.4,
            "api_response": 0.3,
            "cache_age": 0.3,
        }

    def calculate_api_response_score(
        self, status_code: int, response_time: float
    ) -> float:
        """Calculate a score based on API response quality."""
        if status_code == 200:
            status_score = 1.0
        elif status_code in (201, 202, 203):
            status_score = 0.9
        elif status_code in (429, 503):
            status_score = 0.3
        else:
            status_score = 0.5

        time_score = max(
            0.0, min(1.0, (5.0 - response_time) / 4.5)
        )
        return (status_score * 0.7) + (time_score * 0.3)

    def calculate_cache_age_score(self, timestamp: datetime) -> float:
        """Calculate a score based on cache age."""
        age = (datetime.now() - timestamp).total_seconds()
        max_age = 24 * 3600  # 24 hours
        return max(0.0, 1.0 - (age / max_age))

    def update_platform_reliability(
        self,
        platform: str,
        success: bool,
        response_time: Optional[float] = None,
    ) -> None:
        """Update reliability stats for a platform."""
        if platform not in self.platform_scores:
            return

        reliability = self.platform_scores[platform]
        alpha = 0.01  # smoothing factor

        reliability.success_rate = (
            reliability.success_rate * (1 - alpha)
            + (1.0 if success else 0.0) * alpha
        )

        if not success:
            reliability.last_failure = datetime.now()
            if response_time and response_time > 5.0:
                reliability.api_timeouts += 1

    def get_confidence_score(
        self,
        platform: str,
        status_code: int,
        response_time: float,
        cache_timestamp: Optional[datetime] = None,
    ) -> float:
        """Compute the global confidence score of a verification."""
        reliability = self.platform_scores.get(
            platform, PlatformReliability()
        )

        platform_score = (
            reliability.base_score
            * reliability.success_rate
            * (0.9 ** reliability.api_timeouts)
        )

        api_score = self.calculate_api_response_score(
            status_code, response_time
        )

        cache_score = (
            self.calculate_cache_age_score(cache_timestamp)
            if cache_timestamp
            else 1.0
        )

        final_score = (
            platform_score * self.weights["platform_reliability"]
            + api_score * self.weights["api_response"]
            + cache_score * self.weights["cache_age"]
        )

        return round(final_score, 2)
