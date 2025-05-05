📱 Modern Phone Checker

A modern and ethical Python solution for verifying phone numbers on social networks.

This project allows you to quickly and efficiently check whether a phone number is registered on various platforms like WhatsApp, Telegram, Instagram, and Snapchat, while respecting best practices and API limitations.

---

✨ Features

🚀 Optimal Performance

Asynchronous architecture for ultra-fast verification
Smart caching system with freshness score
Built-in rate limiting to respect API limits

🔐 Security & Ethics

Ethical verification without notifying users
Full GDPR compliance
Secure handling of sensitive data

📱 Supported Platforms

WhatsApp – Verification via wa.me API
Telegram – Discreet presence detection
Instagram – Associated profile lookup
Snapchat – Account existence verification

---

🚀 Installation

🧬 Clone the repository

`bash
git clone https://github.com/nabz0r/modern-phone-checker.git
cd modern-phone-checker
`

🧪 Create the virtual environment

`bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
`

📦 Install dependencies

`bash
pip install -r requirements.txt
`

---

💡 Usage

📲 In the command line:

Verify a number:

`bash
python -m phone_checker check +33612345678
`

Launch the REST API:

`bash
python -m phone_checker serve
`

---

🐍 As a Python library:

python
from phone_checker import PhoneChecker

async def check_number():
    checker = PhoneChecker()
    await checker.initialize()

    results = await checker.check_number(
        phone="612345678",
        country_code="33"
    )

    for result in results:
        print(f"{result.platform}: {'✅' if result.exists else '❌'}")
`

---

🧱 Architecture

The project is designed in a modular way:

`
modern-phone-checker/
│
├── phone_checker/         # Main source code
│   ├── core.py            # Core logic
│   ├── cache.py           # Smart caching system
│   ├── models.py          # Data models
│   └── platforms/         # Platform-specific verifiers
│
├── tests/                 # Unit and integration tests
└── docs/                  # Detailed documentation
`

---

🤝 Contribution

Contributions are welcome! Feel free to:

🐛 Report bugs
💡 Suggest features
🔧 Submit pull requests

---

📬 Contact

📧 Email: nabz0r@gmail.com
💻 GitHub: @nabz0r

---

📄 License

MIT License – © 2025 nabz0r