FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Create output directory
RUN mkdir -p output input

# Set environment
ENV PYTHONUNBUFFERED=1

# Run the scraper
CMD ["python", "main.py"]
