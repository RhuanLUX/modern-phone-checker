# Dockerfile

# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create cache directory so our CacheManager can write to it
RUN mkdir -p .cache

# Copy metadata and source code
COPY setup.py requirements.txt ./
COPY modern_phone_checker ./modern_phone_checker

# Install package
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir .

# Define entrypoint
ENTRYPOINT ["modern-phone-checker"]
CMD ["--help"]
