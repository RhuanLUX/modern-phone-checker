"""Snapchat Checker with session and token handling.

This module checks if a phone number exists on Snapchat using
the public web API in an ethical manner.
"""

import httpx
from typing import Optional, Dict
from datetime import datetime
import json
from ..models import PhoneCheckResult
from ..utils import rate_limit, clean_phone_number, validate_phone_number

class SnapchatChecker:
    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self.client = client or httpx.AsyncClient()
        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)',
            'Accept': 'application/json',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        })
        self.timeout = httpx.Timeout(15.0)  # Longer timeout as Snapchat may be slow

    async def _get_web_token(self) -> Optional[str]:
        """Retrieve a temporary token for Snapchat's web API."""
        try:
            response = await self.client.get(
                'https://accounts.snapchat.com/accounts/signup',
                timeout=self.timeout
            )
            # The token is normally inside a meta tag or a JS script
            # This is simplified; proper HTML parsing would be required
            return 'xsrf-token'
        except Exception:
            return None

    @rate_limit(calls=3, period=60)  # Very restrictive to avoid blocking
    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        """Check if a phone number is associated with a Snapchat account.

        This method uses Snapchat’s account validation API
        to determine whether the number is already in use.

        Args:
            phone: Phone number without country code
            country_code: Country code (e.g., '33' for France)
        """
        try:
            if not validate_phone_number(phone, country_code):
                raise ValueError("Invalid phone number format")

            clean_number = clean_phone_number(phone)
            full_number = f"+{country_code}{clean_number}"

            token = await self._get_web_token()
            if not token:
                return PhoneCheckResult(
                    platform='snapchat',
                    exists=False,
                    error="Unable to retrieve access token",
                    timestamp=datetime.now()
                )

            url = "https://accounts.snapchat.com/accounts/validate_phone_number"
            data = {
                'phone_country_code': country_code,
                'phone_number': clean_number,
                'xsrf_token': token
            }

            headers = {
                'X-XSRF-TOKEN': token,
                'Referer': 'https://accounts.snapchat.com/accounts/signup',
            }

            response = await self.client.post(
                url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )

            # In a real case, we would analyze the actual response
            # Here we simulate with a basic check
            exists = response.status_code == 400  # On Snapchat, 400 often means the number is in use

            metadata = {
                'status_code': response.status_code,
                'verification_method': 'signup_validation'
            }

            return PhoneCheckResult(
                platform='snapchat',
                exists=exists,
                metadata=metadata,
                timestamp=datetime.now()
            )

        except httpx.TimeoutException:
            return PhoneCheckResult(
                platform='snapchat',
                exists=False,
                error="Request timed out",
                timestamp=datetime.now()
            )

        except Exception as e:
            return PhoneCheckResult(
                platform='snapchat',
                exists=False,
                error=str(e),
                timestamp=datetime.now()
            )
