"""Data models for the Phone Checker.

This module defines the main data structures used in the application.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class PhoneCheckResult:
    """Result of a phone number check on a specific platform.

    Attributes:
        platform: Name of the platform checked (e.g., 'whatsapp', 'telegram')
        exists: True if the number exists on the platform
        error: Error message if the check failed
        username: Associated username if available
        last_seen: Last activity timestamp if available
        metadata: Additional platform-specific data
        timestamp: Date and time of the check
    """
    platform: str
    exists: bool
    error: Optional[str] = None
    username: Optional[str] = None
    last_seen: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = None

    def __post_init__(self):
        """Initialize the timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
