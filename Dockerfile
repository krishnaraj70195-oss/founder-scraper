FROM node:20-bookworm

WORKDIR /app

# Install Python 3.11
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

# Install browsers for crawl4ai
RUN npx -y playwright install-deps && \
    python3 -m playwright install chromium

# Copy all app files
COPY . .

# Create output directory
RUN mkdir -p output input

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/app/.playwright

# Run the scraper
CMD ["python3", "main.py"]
