from setuptools import setup, find_packages

setup(
    name="modern_phone_checker",
    version="1.1.0",
    description="Check phone and email presence on social networks",
    author="Rhuan, Nabil",
    author_email="rhuan.projetos@gmail.com",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "rich>=13.0",
        "httpx>=0.24",
        "aiohttp-client-cache>=0.8.2",
        "aiofiles>=23.2.1",
        "dnspython>=2.7.0",
        "phonenumbers>=8.12.55",
    ],
    entry_points={
        "console_scripts": [
            "modern-phone-checker=modern_phone_checker.__main__:cli",
        ],
    },
    python_requires=">=3.8",
)
