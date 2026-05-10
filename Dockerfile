FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for crawl4ai (browser support)
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-driver \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install chromium

# Copy all app files
COPY . .

# Create output directory
RUN mkdir -p output input

# Set environment
ENV PYTHONUNBUFFERED=1

# Run the scraper
CMD ["python3", "main.py"]
