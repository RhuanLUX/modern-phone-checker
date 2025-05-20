from .base import BaseChecker
from ..models import PhoneCheckResult


class SnapchatChecker(BaseChecker):
    """Checker for Snapchat profiles."""

    def __init__(self, client, api_key: str = None, cache=None):
        super().__init__(client, api_key=api_key, cache=cache)
        self.endpoint = (
            "https://kit.snapchat.com/v1/contacts"
        )

    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        """
        Perform a Snapchat existence check by phone.
        """
        headers = (
            {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        )
        payload = {"contact": f"+{country_code}{phone}"}
        try:
            resp = await self.client.post(
                self.endpoint, json=payload, headers=headers
            )
            data = resp.json()
            exists = data.get("exists", False)
            return self.create_result(
                platform="snapchat",
                exists=exists,
                metadata={"status_code": resp.status_code}
            )
        except Exception as e:
            return self.create_result(
                platform="snapchat",
                exists=False,
                error=str(e)
            )
