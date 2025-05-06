"""Package containing platform-specific checkers.

Each module in this package implements the verification logic
for a specific platform.
"""

from .whatsapp import WhatsAppChecker
from .telegram import TelegramChecker
from .instagram import InstagramChecker
from .snapchat import SnapchatChecker

# Mapping of available checkers
AVAILABLE_CHECKERS = {
    'whatsapp': WhatsAppChecker,
    'telegram': TelegramChecker,
    'instagram': InstagramChecker,
    'snapchat': SnapchatChecker,
}

# List of default enabled platforms
DEFAULT_PLATFORMS = ['whatsapp', 'telegram', 'instagram', 'snapchat']
