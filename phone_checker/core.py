"""Main module of the phone number checker with cache management.

This module coordinates the platform-specific checkers and handles
the core logic of the application, including the caching system.
"""

import asyncio
from typing import List, Optional, Dict, Any
import httpx
from datetime import datetime

from .models import PhoneCheckResult
from .platforms import AVAILABLE_CHECKERS, DEFAULT_PLATFORMS
from .cache import CacheManager
from .utils import validate_phone_number, clean_phone_number

class PhoneChecker:
    """Main class for phone number verification."""

    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        proxy_url: Optional[str] = None,
        use_cache: bool = True,
        cache_expire: int = 3600
    ):
        """Initializes the checker with the specified options.

        Args:
            platforms: List of platforms to check (all if None)
            proxy_url: Optional proxy URL
            use_cache: Whether to enable the cache system
            cache_expire: Cache expiration duration in seconds
        """
        self.client = httpx.AsyncClient(proxies=proxy_url)
        self.checkers: Dict[str, Any] = {}
        self.use_cache = use_cache

        if use_cache:
            self.cache = CacheManager(expire_after=cache_expire)

        self._initialize_checkers(platforms or DEFAULT_PLATFORMS)

    async def initialize(self):
        """Initializes asynchronous components like the cache."""
        if self.use_cache:
            await self.cache.initialize()

    def _initialize_checkers(self, platforms: List[str]):
        """Initializes the checkers for the selected platforms."""
        for platform in platforms:
            if platform in AVAILABLE_CHECKERS:
                checker_class = AVAILABLE_CHECKERS[platform]
                self.checkers[platform] = checker_class(self.client)

    async def check_number(
        self,
        phone: str,
        country_code: str,
        force_refresh: bool = False
    ) -> List[PhoneCheckResult]:
        """Checks a phone number across all configured platforms.

        Args:
            phone: Phone number without country code
            country_code: Country code (e.g. '33' for France)
            force_refresh: Force fresh verification even if cached

        Returns:
            List of results for each platform
        """
        if not validate_phone_number(phone, country_code):
            raise ValueError(f"Invalid number: +{country_code}{phone}")

        clean_number = clean_phone_number(phone)

        if self.use_cache and not force_refresh:
            cached_results = await self.cache.get(clean_number, country_code)
            if cached_results:
                for result in cached_results['results'].values():
                    if result.metadata is None:
                        result.metadata = {}
                    result.metadata['cached'] = True
                    result.metadata['freshness_score'] = cached_results['freshness_score']
                return list(cached_results['results'].values())

        tasks = [
            checker.check(clean_number, country_code)
            for checker in self.checkers.values()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = [
            r for r in results
            if isinstance(r, PhoneCheckResult)
        ]

        if self.use_cache:
            results_dict = {
                r.platform: r for r in valid_results
            }
            await self.cache.set(clean_number, country_code, results_dict)

        return valid_results

    async def invalidate_cache(self, phone: str, country_code: str):
        """Invalidates the cache for a specific number."""
        if self.use_cache:
            await self.cache.invalidate(phone, country_code)

    async def close(self):
        """Properly closes HTTP connections."""
        await self.client.aclose()
