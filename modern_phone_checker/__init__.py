"""
Phone Checker – A modern and ethical phone number verification tool.
"""

from .core import PhoneChecker  # noqa: F401
from .models import PhoneCheckResult  # noqa: F401

__all__ = ["PhoneChecker", "PhoneCheckResult"]

__version__ = "0.1.0"
