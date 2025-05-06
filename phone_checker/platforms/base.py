from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any
from ..models import PhoneCheckResult

class BaseChecker(ABC):
    def __init__(self, client):
        self.client = client

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
