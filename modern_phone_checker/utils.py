"""Utilities for phone number verification.

This module provides utility functions to:
- Validate phone numbers
- Handle rate limiting
- Clean phone data
"""

import re
from typing import Optional
from functools import wraps
import asyncio
from datetime import datetime, timedelta

def clean_phone_number(phone: str) -> str:
    """Cleans a phone number by removing non-digit characters.

    Args:
        phone: Phone number potentially containing spaces, dashes, etc.

    Returns:
        Cleaned number containing only digits
    """
    return re.sub(r'\D', '', phone)

def validate_phone_number(phone: str, country_code: str) -> bool:
    """Validates a phone number for a given country.

    Args:
        phone: Phone number without country code
        country_code: Country code (e.g., '33' for France)

    Returns:
        True if the number is valid, False otherwise
    """
    # Country-specific patterns (simplified example)
    country_formats = {
        '33': r'^[67]\d{8}$',  # France: mobile starts with 6 or 7, followed by 8 digits
        '1': r'^\d{10}$',      # USA/Canada: 10 digits
    }

    clean_number = clean_phone_number(phone)
    pattern = country_formats.get(country_code)

    if not pattern:
        return True  # Accept if we don't know the country's format

    return bool(re.match(pattern, clean_number))

class RateLimiter:
    """Rate limiter for API requests."""

    def __init__(self, calls: int, period: int):
        """Initializes the rate limiter.

        Args:
            calls: Number of allowed calls
            period: Time period in seconds
        """
        self.calls = calls
        self.period = period
        self.timestamps = []

    async def acquire(self):
        """Waits if necessary to respect the rate limits."""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.period)

        # Remove outdated timestamps
        self.timestamps = [ts for ts in self.timestamps if ts > cutoff]

        if len(self.timestamps) >= self.calls:
            # Wait for the oldest slot to expire
            sleep_time = (self.timestamps[0] - cutoff).total_seconds()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            self.timestamps.pop(0)

        self.timestamps.append(now)

def rate_limit(calls: int, period: int):
    """Decorator to apply rate limiting to an async function.

    Args:
        calls: Number of allowed calls
        period: Time period in seconds
    """
    limiter = RateLimiter(calls, period)

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await limiter.acquire()
            return await func(*args, **kwargs)
        return wrapper

    return decorator
