from .base import BaseChecker
from ..models import PhoneCheckResult


class WhatsAppChecker(BaseChecker):
    """Checker for WhatsApp profiles."""

    def __init__(self, client, api_key: str = None, cache=None):
        """
        Args:
            client:  httpx.AsyncClient instance
            api_key: optional API key (not used for free endpoints)
            cache:   optional CacheManager instance
        """
        super().__init__(client, api_key=api_key, cache=cache)
        self.endpoint = "https://api.whatsapp.com/check"

    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        """
        Perform a WhatsApp existence check.
        """
        # Example request; adapt to real API
        params = {"phone": f"+{country_code}{phone}"}
        try:
            resp = await self.client.get(self.endpoint, params=params)
            exists = (
                resp.status_code == 200 and
                resp.json().get("exists", False)
            )
            return self.create_result(
                platform="whatsapp",
                exists=exists,
                metadata={"status_code": resp.status_code}
            )
        except Exception as e:
            return self.create_result(
                platform="whatsapp",
                exists=False,
                error=str(e)
            )
