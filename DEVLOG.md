# 📘 DEVLOG – Modern Phone Checker

## 📅 Day 1 – May 5, 2025

### ✅ Technical Progress:

- Installed Python 3.13.2  
- Created and activated virtual environment (`.\venv\Scripts\activate`)  
- Installed Rust to compile advanced Python packages  
- Replaced `pydantic==2.4.2` with `pydantic==1.10.13` for compatibility  
- Created a clean and functional `requirements.txt`  
- Successfully installed all dependencies  
- Configured Git with `user.name` and `user.email`  
- First commit and push completed to forked repository  

---

### 🌐 Git and Python Commands Used:

| Command | Description |
|--------|-------------|
| `python -m venv venv` | Creates the virtual environment. |
| `.\venv\Scripts\activate` | Activates the virtual environment on Windows. |
| `pip install -r requirements.txt` | Installs the dependencies. |
| `git config --global user.name "Your Name"` | Sets the Git user name. |
| `git config --global user.email "email@example.com"` | Sets the Git email address. |
| `git add .` | Stages all modified files for commit. |
| `git commit -m "message"` | Saves a commit with a message. |
| `git push origin main` | Sends the commits to GitHub. |

---

# ✅ Daily Development Log

## 📅 Day 1 – May 6, 2025

* 🔤 Full translation of the project to English, including:

  * All `.py` file comments
  * CLI messages and prompts
  * Error messages and field names
* 📦 Renamed the project folder from `modern-phone-checker` to `modern_phone_checker` to enable proper `python -m` module execution
* 🧠 Fixed **relative import issues** and organized the module structure
* ✅ Successfully ran the following command:

  `bash
  python -m phone_checker check 612345678 --country 33
  `

  and confirmed visual output in the terminal
* 💾 Verified that the **smart caching system** works correctly
* 🧪 Performed end-to-end tests to ensure functionality remained intact after translation

At this point, the project is stable, modular, and running locally with full support for the 4 original platforms (WhatsApp, Telegram, Instagram, Snapchat).

---

# ✅ Daily Development Log

## 📅 Day 3 – May 19, 2025

* 🔧 **Docker**

  * Added optimized `Dockerfile` (creates `.cache` directory before installing dependencies).
  * Container builds successfully and runs CLI in the following modes:

    * `--help` (display help)
    * `check --phone` (phone check)
    * `check --email` (email check with `--api-key`).

* 🚀 **CI/CD**

  * Created GitHub Actions workflow `.github/workflows/ci.yml`:

    * **lint-test** job: sets up venv, installs deps, runs flake8 and pytest.
    * **docker** job: builds Docker image using Buildx caching.
  * Added **mock-based testing module** to simulate `PhoneChecker` and `EmailChecker`:

    * Utilizes `pytest-asyncio` and monkeypatch to inject dummy classes.
    * Covers test scenarios with and without cache.

* 📦 **Packaging & Installation**

  * Configured `setup.py` with entry point `modern-phone-checker` in `__main__.py`.
  * Updated `requirements.txt` to include necessary dependencies (httpx, aiofiles, click, rich, dns, phonenumbers).
  * Verified installation in a clean venv and via built wheel (`pip install dist/modern_phone_checker-1.1.0-py3-none-any.whl`).

* 🐞 **Bug Fixes**

  * Fixed “No module named 'modern\_phone\_checker'” error in Docker.
  * Ensured `.cache` directory exists in container to avoid `FileNotFoundError`.
  * Adjusted `CacheManager` and directory creation at build-time.

---

### Next Steps

1. Automate publication to PyPI and Docker Hub via GitHub Actions.
2. Implement `serve` subcommand to launch a REST API.
3. Add new platform checkers (LinkedIn, TikTok, etc.).
