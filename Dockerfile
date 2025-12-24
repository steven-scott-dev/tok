# Use Playwright Python image (with browsers preinstalled)
FROM mcr.microsoft.com/playwright/python:latest

# Set working directory inside the container
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY watcher.py .
COPY login_once.py .

# Make sure Playwright browsers are installed
RUN playwright install --with-deps

# Default command to run your watcher
CMD ["python", "watcher.py"]
