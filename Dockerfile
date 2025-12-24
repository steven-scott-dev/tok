FROM mcr.microsoft.com/playwright:focal

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN playwright install chromium

CMD ["python3", "watcher.py"]
