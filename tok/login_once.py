from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    # 👇 THIS is headed mode
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()

    # Go to TokPortal login
    page.goto("https://app.tokportal.com/account-manager/dashboard")

    print("👉 Log in manually using Google.")
    print("👉 When you are fully logged in and see your dashboard, come back here.")

    # Pause the script so YOU can log in
    input("Press ENTER here after login is complete...")

    # Save cookies
    cookies = context.cookies()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

    print("✅ Cookies saved to cookies.json")

    browser.close()
