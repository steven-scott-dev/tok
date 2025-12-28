        # Container selector
        container_selector = "div.bg-white.rounded-lg.p-8.text-center"
        container = page.locator(container_selector)
        children = container.locator("> *").all()

        current_count = len(children)
        if current_count > last_count:
            notify(f"🔥 NEW TokPortal mission(s)! Count: {current_count - last_count}")
            last_count = current_count
            save_last_count(last_count)
        else:
            print("No new missions yet")

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
                # Attempt to reload the page safely
                try:
                    page.reload(timeout=15000)
                except playwright._impl._errors.TimeoutError:
                    print("Page reload timed out, continuing...")

                # Check if container exists and get children
                if container.is_visible():
                    children = container.locator("> *").all()
                else:
                    children = []

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

                # Check again in 30 seconds
                time.sleep(30)

            except Exception as e:
                print(f"Error during check: {e}")
                time.sleep(60)

        # Debug info for push notifications credentials (optional)
        print("Loaded:", repr(PUSHOVER_USER), repr(PUSHOVER_TOKEN))