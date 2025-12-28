# Use the official Playwright Python image so browsers are preinstalled
FROM mcr.microsoft.com/playwright/python:latest

# Set workdir
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY watcher.py .
COPY login_once.py .

# Make sure playwright browsers are installed (if not in base image)
RUN playwright install --with-deps

# Run watcher
CMD ["python", "watcher.py"]
