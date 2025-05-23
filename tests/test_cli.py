import pytest
from datetime import datetime
from click.testing import CliRunner

from modern_phone_checker.__main__ import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_check_help_shows_options(runner):
    result = runner.invoke(cli, ["check", "--help"])
    assert result.exit_code == 0
    assert "--phone" in result.output
    assert "--email" in result.output
    assert "--api-key" in result.output

def test_help_shows_commands(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "check" in result.output

def test_check_phone_only(runner, monkeypatch):
    class DummyChecker:
        def __init__(self, *args, **kwargs):
            pass
        async def check_number(self, phone, country, force_refresh=False):
            from modern_phone_checker.models import PhoneCheckResult
            return [
                PhoneCheckResult(
                    platform="dummy",
                    exists=True,
                    username=None,
                    metadata={},
                    error=None,
                    timestamp=datetime(2025, 1, 1, 0, 0, 0),
                )
            ]
        async def close(self):
            pass

    monkeypatch.setattr(
        "modern_phone_checker.__main__.PhoneChecker",
        DummyChecker
    )

    result = runner.invoke(cli, ["check", "--phone", "612345678"])
    assert result.exit_code == 0
    assert "DUMMY" in result.output

def test_check_email_only(runner, monkeypatch):
    class DummyEmail:
        def __init__(self, *args, **kwargs):
            pass
        async def check(self, email):
            from modern_phone_checker.models import PhoneCheckResult
            return PhoneCheckResult(
                platform="email",
                exists=True,
                username=None,
                metadata={"valid_syntax": True, "valid_mx": True},
                error=None,
                timestamp=datetime(2025, 1, 1, 0, 0, 0),
            )

    monkeypatch.setattr(
        "modern_phone_checker.__main__.EmailChecker",
        DummyEmail
    )

    result = runner.invoke(
        cli,
        ["check", "--email", "example@domain.com", "--api-key", "DUMMY"]
    )
    assert result.exit_code == 0
    assert "EMAIL" in result.output
    assert "valid_syntax" in result.output

def test_check_email_without_api_key(runner):
    """Should show warning and skip email check if no API key."""
    result = runner.invoke(
        cli,
        ["check", "--email", "example@domain.com"]
    )
    assert result.exit_code == 0
    assert (
        "Email checking requires an API key. Skipping email check."
        in result.output
    )
