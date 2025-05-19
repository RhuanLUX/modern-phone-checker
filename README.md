# 📱 Modern Phone Checker

> Une solution Python moderne et éthique pour la vérification des numéros de téléphone sur les réseaux sociaux.

Ce projet permet de vérifier rapidement et efficacement si un numéro de téléphone est enregistré sur différentes plateformes comme WhatsApp, Telegram, Instagram et Snapchat, tout en respectant les bonnes pratiques et les limitations d'API.

## ✨ Caractéristiques

🚀 **Performances Optimales**
- Architecture asynchrone pour des vérifications ultra-rapides
- Système de cache intelligent avec score de fraîcheur 
- Rate limiting intégré pour respecter les limites des APIs

🛡️ **Sécurité & Éthique**
- Vérifications éthiques sans notifications aux utilisateurs
- Respect complet du RGPD
- Gestion sécurisée des données sensibles

🎯 **Plateformes Supportées**
- WhatsApp - Vérification via l'API wa.me
- Telegram - Détection de présence discrète
- Instagram - Recherche de profil associé
- Snapchat - Vérification de l'existence du compte

## 🚀 Installation

```bash
# Cloner le repository
git clone https://github.com/nabz0r/modern-phone-checker.git
cd modern-phone-checker

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 💡 Utilisation

En ligne de commande :
```bash
# Vérifier un numéro
python -m phone_checker check +33612345678

# Lancer l'API REST
python -m phone_checker serve
```

En tant que bibliothèque Python :
```python
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
```

## 🏗️ Architecture

Le projet est conçu de manière modulaire avec :

```
modern-phone-checker/
├── phone_checker/         # Code source principal
│   ├── core.py           # Logique centrale
│   ├── cache.py          # Système de cache intelligent
│   ├── models.py         # Modèles de données
│   └── platforms/        # Vérificateurs par plateforme
├── tests/                # Tests unitaires et d'intégration
└── docs/                 # Documentation détaillée
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des fonctionnalités
- 🔧 Soumettre des pull requests

## 📬 Contact

- 📧 Email : nabz0r@gmail.com
- 🐙 GitHub : [@nabz0r](https://github.com/nabz0r)

## 📝 Licence

MIT License - © 2025 nabz0r

----------------------------------------------------------------------------------- by @ Rhuan

# Modern Phone Checker

Check phone numbers and email addresses across popular social platforms from the command line, with caching and a mock monetization flow.

---

Features

✅ Phone lookup on WhatsApp, Telegram, Instagram, and Snapchat
📧 Email validation (syntax + MX lookup)
💾 **Async cache (configurable expiration)
🔒 Mock monetization: free vs. paid flows via `--api-key`
🚀 Rich CLI output with tables, panels, and status indicators
🔧 Fully typed with dataclasses, MyPy-compatible

---

## Installation

```bash
# Clone the repo
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
# Install the package in editable mode
pip install -e .
```

Or install from PyPI:

```bash
pip install modern_phone_checker
```

---

## Usage

```bash
modern-phone-checker --help
```

### Checking a phone number (Free)

By default, only **WhatsApp** and **Telegram** checks run without an API key:

```bash
modern-phone-checker check --phone 612345678
```

### Checking with a specific country code

Default country code is **33 (France)**. To check Luxembourg or Brazil:

```bash
modern-phone-checker check --phone 691234567 --country 352  # Luxembourg
modern-phone-checker check --phone 11999998888 --country 55  # Brazil
```

### Premium flow (all platforms + email)

Provide an API key to unlock all checks (Instagram, Snapchat, Email):

```bash
modern-phone-checker check \
  --phone 612345678 \
  --email example@domain.com \
  --api-key YOUR_KEY_HERE
```

### Force refresh (ignore cache)

```bash
modern-phone-checker check --phone 612345678 --force-refresh
```

### Custom cache expiration

```bash
modern-phone-checker check --phone 612345678 --cache-expire 600
```

---

## Options

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

## Contributing

Feel free to open issues or pull requests. For development:

```bash
# run tests
gpytest -q
```

---

## License

MIT © Rhuan Pablo da Silva
