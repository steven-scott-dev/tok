from playwright.sync_api import sync_playwright
import time
import requests
import json
import os


# ------------------------------
# Pushover setup
# ------------------------------
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

def notify(msg):
    try:
        r = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_TOKEN,
                "user": PUSHOVER_USER,
                "message": msg,
            },
            timeout=5
        )
        if r.status_code == 200:
            print(f"Notification sent: {msg}")
        else:
            print(f"Failed to send notification, status code: {r.status_code}")
    except Exception as e:
        print(f"Error sending notification: {e}")

# ------------------------------
# Load cookies
# ------------------------------

cookies_data = os.environ.get("COOKIES_JSON")
if not cookies_data:
    raise Exception("COOKIES_JSON secret not set!")

cookies = json.loads(cookies_data)
# ------------------------------
# Load last count from file
# ------------------------------
STATE_FILE = "last_count.json"
def load_last_count():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f).get("last_count", 0)
        except:
            return 0
    return 0

def save_last_count(count):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_count": count}, f)

# ------------------------------
# Watcher
# ------------------------------
def main():
    last_count = load_last_count()
    print(f"Loaded last count: {last_count}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        page.goto("https://app.tokportal.com/account-manager/dashboard", wait_until="networkidle")

        # Container selector
        container_selector = "div.bg-white.rounded-lg.p-8.text-center"
        container = page.locator(container_selector)

        # Initial debug info
        children = container.locator("> *").all()
        current_count = len(children)
        print(f"Starting watcher. Container children: {current_count}")
        for i, child in enumerate(children):
            if i < 3:
                print(f"Child {i}: {child.inner_text()}")

        # Immediate test notification
        notify("🔥 TEST: Watcher is working")

        # Optional: force a test change if container empty
        if current_count == 0:
            print("Container empty — forcing test notification")
            notify("🔥 TEST: Simulated new mission!")

        # Update last_count for first run
        if current_count > last_count:
            last_count = current_count
            save_last_count(last_count)

        while True:
            try:
                page.reload(wait_until="networkidle")
                children = container.locator("> *").all()
                current_count = len(children)

                # Debug info
                print(f"Current children count: {current_count}")
                for i, child in enumerate(children):
                    if i < 3:
                        print(f"Child {i}: {child.inner_text()}")

                # Notify if new items appeared
                if current_count > last_count:
                    notify(f"🔥 NEW TokPortal mission(s)! Count: {current_count - last_count}")
                    last_count = current_count
                    save_last_count(last_count)

                time.sleep(30)  # check every 30 seconds

            except Exception as e:
                print(f"Error during check: {e}")
                time.sleep(60)

if __name__ == "__main__":
    main()
