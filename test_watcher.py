from playwright.sync_api import sync_playwright
import time
import requests
import os

# Pushover setup
PUSHOVER_USER = os.getenv("urbaeip9m5ohqs46yn9xpch2eeu115")
PUSHOVER_TOKEN = os.getenv("aqogjeaxapgfy6b7hx9k343i35ybf3aqogjeaxapgfy6b7hx9k343i35ybf3")

def notify(msg):
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_TOKEN,
                "user": PUSHOVER_USER,
                "message": msg,
            },
            timeout=5
        )
        print("Notification sent!")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def main():
    # First, test notification immediately
    notify("🔥 TEST: Watcher is working")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://example.com")

        last_title = page.title()
        print(f"Starting watcher, initial title: {last_title}")

        while True:
            page.reload()
            current_title = page.title()
            if current_title != last_title:
                notify("🔥 Page changed!")
                print(f"Page changed! New title: {current_title}")
                last_title = current_title
            time.sleep(10)  # check every 10 seconds

if __name__ == "__main__":
    main()
