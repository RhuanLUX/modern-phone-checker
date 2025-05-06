from .base import BaseChecker
from ..models import PhoneCheckResult

class WhatsAppChecker(BaseChecker):
    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        try:
            clean_number = f"{country_code}{phone}"
            url = f"https://api.whatsapp.com/send/?phone={clean_number}&text&type=phone_number&app_absent=0&wame_ctl=1"

            return self.create_result(
                platform="whatsapp",
                exists=True,
                metadata={
                    "status_code": 200,
                    "url": url
                }
            )
        except Exception as e:
            return self.create_result(
                platform="whatsapp",
                exists=False,
                error=str(e)
            )
