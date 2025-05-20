"""EmailChecker: syntax + MX record validation returning PhoneCheckResult."""

import re
import dns.resolver
from datetime import datetime

from .models import PhoneCheckResult


class EmailChecker:
    """Checks an email address for valid syntax and MX records."""

    def __init__(self, api_key: str = None, cache=None):
        """
        Args:
            api_key: Optional API key for premium email-verification services.
            cache: Optional CacheManager (not used in this simple checker).
        """
        self.api_key = api_key
        self.cache = cache

    def check(self, email: str) -> PhoneCheckResult:
        """
        Perform a two-step email check:
          1) Regex syntax validation.
          2) MX lookup on the domain.

        Returns:
            PhoneCheckResult with:
              - platform="email"
              - exists=True only if both syntax and MX pass
              - metadata={"valid_syntax":…, "valid_mx":…}
              - error=str(exception) if MX lookup raises
              - timestamp=datetime.now()
        """
        # 1) Syntax check
        regex = r"[^@]+@[^@]+\.[^@]+"
        syntax_ok = bool(re.fullmatch(regex, email))

        # 2) MX check
        valid_mx = False
        error = None
        if syntax_ok:
            try:
                domain = email.split("@", 1)[1]
                answers = dns.resolver.resolve(domain, "MX")
                valid_mx = len(answers) > 0
            except Exception as e:
                error = str(e)

        # Build metadata dict
        metadata = {
            "valid_syntax": syntax_ok,
            "valid_mx": valid_mx
        }

        return PhoneCheckResult(
            platform="email",
            exists=(syntax_ok and valid_mx),
            username=None,
            metadata=metadata,
            error=error,
            timestamp=datetime.now()
        )
