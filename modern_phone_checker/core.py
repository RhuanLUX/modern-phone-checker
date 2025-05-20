"""Main module of the phone number checker with cache management.

This module coordinates the platform-specific checkers and handles
the core logic of the application, including the caching system.
"""

import asyncio
from typing import List, Optional, Dict, Any
import httpx

from .models import PhoneCheckResult
from .platforms import AVAILABLE_CHECKERS, DEFAULT_PLATFORMS
from .cache import CacheManager
from .utils import validate_phone_number, clean_phone_number


class PhoneChecker:
    """Main class for phone number verification."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        cache: Optional[CacheManager] = None,
        platforms: Optional[List[str]] = None,
        use_cache: bool = True,
        cache_expire: int = 3600,
    ):
        """
        Initializes the checker with the specified options.

        Args:
            api_key: Optional API key for premium features.
            cache: Optional CacheManager instance (if you want to share cache).
            platforms: List of platforms to check (all if None).
            use_cache: Whether to enable caching.
            cache_expire: Cache expiration duration in seconds.
        """
        # Create an HTTPX AsyncClient (no proxies argument)
        self.client = httpx.AsyncClient()
        self.checkers: Dict[str, Any] = {}
        self.api_key = api_key
        self.use_cache = use_cache

        # Use provided cache manager or create a new one
        if cache is not None:
            self.cache = cache
        elif use_cache:
            self.cache = CacheManager(expire_after=cache_expire)

        # Instantiate platform-specific checkers
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
                # Pass client, api_key, and cache to each checker
                self.checkers[platform] = checker_class(
                    client=self.client,
                    api_key=self.api_key,
                    cache=self.cache if self.use_cache else None
                )

    async def check_number(
        self,
        phone: str,
        country_code: str,
        force_refresh: bool = False
    ) -> List[PhoneCheckResult]:
        """Checks a phone (or email) across all configured platforms.

        Args:
            phone: Phone number without country code.
            country_code: Country code (e.g. '33' for France).
            force_refresh: Force fresh verification even if cached.

        Returns:
            List of results for each platform.
        """
        # Validate the input number
        if not validate_phone_number(phone, country_code):
            raise ValueError(f"Invalid number: +{country_code}{phone}")

        clean_number = clean_phone_number(phone)

        # Return cached results if fresh
        if self.use_cache and not force_refresh:
            cached = await self.cache.get(clean_number, country_code)
            if cached:
                results = []
                for res in cached['results'].values():
                    if res.metadata is None:
                        res.metadata = {}
                    res.metadata['cached'] = True
                    res.metadata['freshness_score'] = cached['freshness_score']
                    results.append(res)
                return results

        # Perform all checks in parallel
        tasks = [
            checker.check(clean_number, country_code)
            for checker in self.checkers.values()
        ]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter valid PhoneCheckResult objects
        valid_results = [
            r for r in raw_results if isinstance(r, PhoneCheckResult)
        ]

        # Save fresh results to cache
        if self.use_cache:
            results_dict = {r.platform: r for r in valid_results}
            await self.cache.set(clean_number, country_code, results_dict)

        return valid_results

    async def invalidate_cache(self, phone: str, country_code: str):
        """Invalidates the cache for a specific number."""
        if self.use_cache:
            await self.cache.invalidate(phone, country_code)

    async def close(self):
        """Properly closes HTTP connections."""
        await self.client.aclose()
