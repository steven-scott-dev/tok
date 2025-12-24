FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY watcher.py .
COPY login_once.py .

RUN playwright install --with-deps

CMD ["python", "watcher.py"]
