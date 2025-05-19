# modern_phone_checker/platforms/telegram.py
from .base import BaseChecker
from ..models import PhoneCheckResult

class TelegramChecker(BaseChecker):
    """Checker for Telegram profiles."""

    def __init__(self, client, api_key: str = None, cache=None):
        super().__init__(client, api_key=api_key, cache=cache)
        self.endpoint = "https://api.telegram.org/bot<token>/getProfilePhotos"

    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        """
        Perform a Telegram existence check by phone.
        """
        # Replace <token> with api_key or other logic
        url = self.endpoint.replace("<token>", self.api_key or "")
        params = {"user_id": f"+{country_code}{phone}"}
        try:
            resp = await self.client.get(url, params=params)
            data = resp.json()
            exists = "result" in data
            return self.create_result(
                platform="telegram",
                exists=exists,
                metadata={"status_code": resp.status_code}
            )
        except Exception as e:
            return self.create_result(
                platform="telegram",
                exists=False,
                error=str(e)
            )
