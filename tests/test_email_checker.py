# tests/test_phone_checker.py
import asyncio
import pytest
from datetime import datetime

from modern_phone_checker.core import PhoneChecker
from modern_phone_checker.models import PhoneCheckResult
from modern_phone_checker.platforms import AVAILABLE_CHECKERS


class DummyChecker:
    """A fake checker that always returns a successful PhoneCheckResult."""
    def __init__(self, client, api_key=None, cache=None):
        self.client = client
        self.api_key = api_key
        self.cache = cache

    async def check(self, phone: str, country_code: str) -> PhoneCheckResult:
        return PhoneCheckResult(
            platform="dummy",
            exists=True,
            username="user123",
            metadata={},
            error=None,
            timestamp=datetime(2025, 1, 1, 0, 0, 0),
        )


@pytest.fixture(autouse=True)
def register_dummy():
    # register the DummyChecker under the key "dummy"
    AVAILABLE_CHECKERS["dummy"] = DummyChecker
    yield
    AVAILABLE_CHECKERS.pop("dummy", None)


@pytest.mark.asyncio
async def test_check_number_without_cache():
    # use a valid French national number (612345678) instead of "123"
    checker = PhoneChecker(platforms=["dummy"], use_cache=False)
    results = await checker.check_number("612345678", "33", force_refresh=False)
    assert isinstance(results, list)
    assert len(results) == 1
    r = results[0]
    assert r.platform == "dummy"
    assert r.exists is True
    assert r.username == "user123"
    await checker.close()


@pytest.mark.asyncio
async def test_check_number_with_cache(tmp_path, monkeypatch):
    # use a valid French national number (612345678) instead of "456"
    cache_dir = tmp_path / "cache"
    checker = PhoneChecker(
        platforms=["dummy"], use_cache=True, cache_expire=60
    )
    checker.cache.cache_dir = cache_dir
    await checker.initialize()

    # first call — writes to cache
    results1 = await checker.check_number("612345678", "33", force_refresh=False)
    assert len(results1) == 1

    # now patch DummyChecker.check to ensure cache is used
    monkeypatch.setattr(
        DummyChecker,
        "check",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("DummyChecker.check should NOT be called"))
    )

    # second call — should come from cache
    results2 = await checker.check_number("612345678", "33", force_refresh=False)
    assert len(results2) == 1
    assert results2[0].metadata.get("cached") is True

    await checker.close()
