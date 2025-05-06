"""Instagram Checker with intelligent request handling.

This module checks if a phone number is associated with an Instagram account
by using the public API in a respectful and ethical way.
"""

import httpx
from typing import Optional
from datetime import datetime
import json
from ..models import PhoneCheckResult
from ..utils import rate_limit, clean_phone_number, validate_phone_number

class InstagramChecker:
    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self.client = client or httpx.AsyncClient()
        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)',
            'Accept': 'application/json',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        })
        self.timeout = httpx.Timeout(10.0)

    @rate_limit(calls=5, period=60)  # More restrictive because Instagram is sensitive to rate limiting
    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        """Check if a number is associated with an Instagram account.

        This method uses the public sign-up API from Instagram to check if
        a number is already linked to an existing account.

        Args:
            phone: Phone number without country code
            country_code: Country code (e.g., '33' for France)
        """
        try:
            if not validate_phone_number(phone, country_code):
                raise ValueError("Invalid phone number format")

            clean_number = clean_phone_number(phone)
            full_number = f"+{country_code}{clean_number}"

            # Endpoint used for sign-up form validation
            url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
            data = {
                'email': '',
                'username': '',
                'first_name': '',
                'opt_into_one_tap': 'false',
                'phone_number': full_number
            }

            # Add specific headers to mimic a legitimate request
            headers = {
                'X-CSRFToken': 'missing',  # Instagram accepts 'missing' for unauthenticated requests
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/emailsignup/'
            }

            response = await self.client.post(
                url,
                data=data,
                headers=headers,
                timeout=self.timeout
            )

            # Response analysis
            result = response.json()
            exists = bool(result.get('errors', {}).get('phone_number'))

            metadata = {
                'status_code': response.status_code,
                'response_type': 'account_exists' if exists else 'number_available'
            }

            return PhoneCheckResult(
                platform='instagram',
                exists=exists,
                metadata=metadata,
                timestamp=datetime.now()
            )

        except json.JSONDecodeError:
            return PhoneCheckResult(
                platform='instagram',
                exists=False,
                error="Failed to parse Instagram response",
                timestamp=datetime.now()
            )

        except httpx.TimeoutException:
            return PhoneCheckResult(
                platform='instagram',
                exists=False,
                error="Request timed out",
                timestamp=datetime.now()
            )

        except Exception as e:
            return PhoneCheckResult(
                platform='instagram',
                exists=False,
                error=str(e),
                timestamp=datetime.now()
            )
