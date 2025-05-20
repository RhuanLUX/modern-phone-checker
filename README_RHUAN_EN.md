# 📱 Modern Phone Checker

[![CI](https://github.com/your-org/modern_phone_checker/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/modern_phone_checker/actions/workflows/ci.yml)

> A modern, ethical Python solution for verifying phone numbers and emails on popular social platforms.

This project allows you to quickly check if a phone number is registered on platforms like WhatsApp, Telegram, Instagram, and Snapchat, following best practices and respecting API limitations. Email verification is also available via a premium API key.

---

## ✨ Features

- **Asynchronous architecture** for ultra-fast checks
- **Smart caching** with freshness scoring
- **Built-in rate limiting** for API compliance
- **Rich CLI** with tables and panels (via [rich](https://github.com/Textualize/rich))
- **Full GDPR compliance** (no user notifications)
- **Secure handling** of sensitive data
- **Phone number checks**: WhatsApp, Telegram, Instagram, Snapchat
- **Email verification**: Syntax & MX (premium feature)

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/your-org/modern_phone_checker.git
cd modern_phone_checker

# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode (optional for development)
pip install -e .
````

Or install from PyPI:

```bash
pip install modern_phone_checker
```

---

## 💡 Usage

### CLI

```bash
modern-phone-checker --help
```

#### Check a phone number (Free)

By default, **WhatsApp** and **Telegram** checks are available without an API key.

```bash
modern-phone-checker check --phone 612345678
```

#### Check with a specific country code

Default is `33` (France). For Luxembourg or Brazil:

```bash
modern-phone-checker check --phone 691234567 --country 352  # Luxembourg
modern-phone-checker check --phone 11999998888 --country 55  # Brazil
```

#### Premium (all platforms + email)

Pass an API key to unlock Instagram, Snapchat, and email checking:

```bash
modern-phone-checker check \
  --phone 612345678 \
  --email example@domain.com \
  --api-key YOUR_KEY_HERE
```

#### Force refresh (ignore cache)

```bash
modern-phone-checker check --phone 612345678 --force-refresh
```

#### Custom cache expiration

```bash
modern-phone-checker check --phone 612345678 --cache-expire 600
```

---

### Python Library

You can use `PhoneChecker` directly in your Python code:

```python
import asyncio
from modern_phone_checker import PhoneChecker

async def main():
    checker = PhoneChecker()
    await checker.initialize()
    results = await checker.check_number(
        phone="612345678",
        country_code="33"
    )
    for result in results:
        print(f"{result.platform}: {'✅' if result.exists else '❌'}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🏗️ Architecture

```
modern_phone_checker/
├── __main__.py           # CLI entry point
├── core.py               # Core phone/email checking logic
├── cache.py              # Smart cache manager
├── email_checker.py      # Email checking logic
├── confidence.py         # Confidence scoring
├── utils.py              # Utility functions
├── platforms/            # Platform-specific checkers
├── tests/                # Unit and integration tests
├── docs/                 # Additional documentation
```

---

## 🛠️ Options

| Flag              | Description                                        |
| ----------------- | -------------------------------------------------- |
| `--phone`         | Phone number in E.164 or national format           |
| `--email`         | Email address to check                             |
| `--country, -c`   | Country code (default: 33 for France)              |
| `--api-key`       | Enable premium checks (Instagram, Snapchat, Email) |
| `--force-refresh` | Ignore cache and run fresh verification            |
| `--cache-expire`  | Cache TTL in seconds (default: 3600)               |
| `--help`          | Show help message                                  |

---

## 🗣️ Notes

* Instagram, Snapchat, and email checks **require** an API key (see premium flow).
* If `--api-key` is **not** provided, these checks will be skipped, and a warning will be displayed.
* A REST API (`--serve`) will be available in a future release (see roadmap).

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

* Report bugs or request features (Issues)
* Submit Pull Requests

To run tests locally:

```bash
pytest
```

---

## 📬 Contact

* GitHub: [@nabz0r](https://github.com/nabz0r)

---

## 📄 License

MIT © Rhuan Pablo da Silva

