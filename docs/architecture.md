# 🧱 System Architecture

## 🔄 Modules
- `phone_checker/` – Core logic, platform coordination.
- `platforms/` – Individual checkers for each platform.
- `cache.py` – Smart caching system with expiration.
- `utils.py` – Phone validation, rate limiting, cleaning.
- `cli.py` – Command-line interface.


## 📦 Folder Structure

modern-phone-checker/
├── phone_checker/
│ ├── init.py
│ ├── core.py
│ ├── platforms/
│ ├── cache.py
│ ├── utils.py
├── main.py
├── requirements.txt
├── README.md
└── docs/


## 📡 Flow
User input ➝ PhoneChecker ➝ Platforms ➝ API requests ➝ Result ➝ Cache ➝ CLI Display
