# modern_phone_checker/platforms/instagram.py
from .base import BaseChecker
from ..models import PhoneCheckResult

class InstagramChecker(BaseChecker):
    """Checker for Instagram profiles."""

    def __init__(self, client, api_key: str = None, cache=None):
        super().__init__(client, api_key=api_key, cache=cache)
        self.endpoint = "https://www.instagram.com/api/v1/users/search/"

    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        """
        Perform an Instagram existence check by phone.
        """
        payload = {"q": f"+{country_code}{phone}"}
        try:
            resp = await self.client.get(self.endpoint, params=payload)
            users = resp.json().get("users", [])
            exists = len(users) > 0
            username = users[0]["username"] if exists else None
            return self.create_result(
                platform="instagram",
                exists=exists,
                username=username,
                metadata={"status_code": resp.status_code}
            )
        except Exception as e:
            return self.create_result(
                platform="instagram",
                exists=False,
                error=str(e)
            )
