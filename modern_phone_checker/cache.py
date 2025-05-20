"""Smart caching system for phone number verifications.

This module temporarily stores verification results to avoid
sending too many API requests. It uses a freshness score to
decide when to refresh the data.
"""

import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import aiofiles
import aiofiles.os
from .models import PhoneCheckResult


class CacheManager:
    def __init__(self, cache_dir: str = '.cache', expire_after: int = 3600):
        """Initialize the cache manager.

        Args:
            cache_dir: Directory to store cache files.
            expire_after: Cache validity duration in seconds (default: 1 hour).
        """
        self.cache_dir = Path(cache_dir)
        self.expire_after = expire_after
        self.cache_data: Dict[str, Any] = {}

    async def initialize(self):
        """Create the cache directory if needed and load existing data."""
        await self._ensure_cache_dir()
        await self._load_cache()

    async def _ensure_cache_dir(self):
        """Ensure the cache directory exists."""
        if not self.cache_dir.exists():
            await aiofiles.os.makedirs(str(self.cache_dir))

    def _get_cache_file(self, phone: str, country_code: str) -> Path:
        """Generate the cache file path for a given number."""
        cache_key = f"{country_code}_{phone}"
        return self.cache_dir / f"{cache_key}.json"

    async def _load_cache(self):
        """Load existing cache data from disk."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                async with aiofiles.open(cache_file, mode='r') as f:
                    content = await f.read()
                    self.cache_data[cache_file.stem] = json.loads(content)
        except Exception as e:
            print(f"Error while loading cache: {e}")

    def _calculate_freshness_score(self, timestamp: datetime) -> float:
        """Calculate a freshness score for cached data.

        The score ranges from 1.0 (very fresh) to 0.0 (expired).
        """
        age = (datetime.now() - timestamp).total_seconds()
        return max(0.0, 1.0 - (age / self.expire_after))

    async def get(
        self,
        phone: str,
        country_code: str
    ) -> Optional[Dict[str, PhoneCheckResult]]:
        """Retrieve cached results for a phone number.

        Returns:
            Cached results if valid, otherwise None.
        """
        cache_key = f"{country_code}_{phone}"
        cached_data = self.cache_data.get(cache_key)

        if not cached_data:
            return None

        timestamp = datetime.fromisoformat(cached_data['timestamp'])
        freshness = self._calculate_freshness_score(timestamp)

        if freshness <= 0:
            await self.invalidate(phone, country_code)
            return None

        cached_data['freshness_score'] = freshness
        cached_data['results'] = {
            platform: PhoneCheckResult(**data)
            for platform, data in cached_data['results'].items()
        }
        return cached_data

    async def set(
        self,
        phone: str,
        country_code: str,
        results: Dict[str, PhoneCheckResult]
    ):
        """Store verification results in cache for a phone number."""
        cache_key = f"{country_code}_{phone}"
        serializable_results = {}

        for platform, result in results.items():
            serializable_results[platform] = {
                "platform": result.platform,
                "exists": result.exists,
                "username": result.username,
                "error": result.error,
                "timestamp": (
                    result.timestamp.isoformat()
                    if result.timestamp else None
                ),
                "metadata": result.metadata,
            }

        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'results': serializable_results
        }

        self.cache_data[cache_key] = cache_data

        cache_file = self._get_cache_file(phone, country_code)
        async with aiofiles.open(cache_file, mode='w') as f:
            await f.write(json.dumps(cache_data, indent=2))

    async def invalidate(self, phone: str, country_code: str):
        """Invalidate cache for a specific number."""
        cache_key = f"{country_code}_{phone}"
        self.cache_data.pop(cache_key, None)

        cache_file = self._get_cache_file(phone, country_code)
        if cache_file.exists():
            await aiofiles.os.remove(str(cache_file))
