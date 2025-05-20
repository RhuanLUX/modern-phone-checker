from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any
from ..models import PhoneCheckResult


class BaseChecker(ABC):
    def __init__(self, client, api_key: Optional[str] = None, cache=None):
        """
        Base class initializer for all platform checkers.

        Args:
            client: an httpx.AsyncClient instance
            api_key: optional API key for premium endpoints
            cache: optional CacheManager for storing results
        """
        self.client = client
        self.api_key = api_key
        self.cache = cache

    @abstractmethod
    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        """Method that each platform must implement."""
        pass

    def create_result(
        self,
        platform: str,
        exists: bool,
        username: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> PhoneCheckResult:
        """Creates a standardized result object."""
        return PhoneCheckResult(
            platform=platform,
            exists=exists,
            username=username,
            metadata=metadata,
            error=error,
            timestamp=datetime.now()
        )
