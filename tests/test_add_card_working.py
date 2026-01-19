"""
Working test for Add Card flow using proper element selection.
"""

import subprocess
import sys
import time
import json
import os
import threading
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent


def run_test():
    print("\n" + "="*70)
    print("ADD CARD WORKING TEST")
    print("="*70 + "\n")

    env = os.environ.copy()
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["PYTHONUNBUFFERED"] = "1"

    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "src/ui/app.py",
         "--server.port", "8599",
         "--server.headless", "true",
         "--browser.gatherUsageStats", "false"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        cwd=str(PROJECT_ROOT),
        text=True,
        bufsize=1
    )

    server_logs = []
    def read_logs():
        for line in process.stdout:
            stripped = line.strip()
            server_logs.append(stripped)
            if "[ChurnPilot]" in stripped and "Load result" not in stripped and "Load returned" not in stripped:
                print(f"  SERVER: {stripped}")

    log_thread = threading.Thread(target=read_logs, daemon=True)
    log_thread.start()

    print("Starting Streamlit app...")
    time.sleep(8)

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(browser, 10)

        url = "http://localhost:8599"

        # Load and clear
        print("[1] Loading page and clearing localStorage...")
        browser.get(url)
        time.sleep(10)
        browser.execute_script("localStorage.clear()")
        browser.refresh()
        time.sleep(10)

        print(f"   localStorage: {browser.execute_script('return localStorage.getItem(\"churnpilot_cards\")')}")

        # Click Add Card tab
        print("\n[2] Clicking Add Card tab...")
        tabs = browser.find_elements(By.CSS_SELECTOR, "[data-baseweb='tab']")
        for tab in tabs:
            if "Add" in tab.text:
                tab.click()
                print(f"   Clicked: {tab.text}")
                break
        time.sleep(3)

        # Find and click the Card selectbox
        print("\n[3] Selecting card from dropdown...")

        # Find the second selectbox (Card selector)
        selectboxes = browser.find_elements(By.CSS_SELECTOR, "[data-testid='stSelectbox']")
        print(f"   Found {len(selectboxes)} selectboxes")

        if len(selectboxes) >= 2:
            card_selectbox = selectboxes[1]

            # Click to open the dropdown
            card_selectbox.click()
            time.sleep(1)

            # Wait for options to appear
            options_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[role='option']")))
            print(f"   Found {len(options_list)} options")

            # Store the text before clicking (element will disappear after click)
            if len(options_list) > 1:
                option_text = options_list[1].text
                print(f"   Selecting: '{option_text}'")
                options_list[1].click()

        # Wait for page to rerender after selection
        print("   Waiting for page to update...")
        time.sleep(5)

        # Find the primary button
        print("\n[4] Looking for Add Card submit button...")

        # Look specifically for primary button that's visible
        buttons = browser.find_elements(By.TAG_NAME, "button")
        primary_btn = None
        for btn in buttons:
            kind = btn.get_attribute("kind") or ""
            visible = btn.is_displayed()
            text = btn.text.strip()

            if kind == "primary" and visible:
                primary_btn = btn
                print(f"   Found visible primary button: text='{text}'")
                break

        if not primary_btn:
            # Try to find it by testid and scroll into view
            print("   Primary button not visible, trying to find by testid...")
            primary_btns = browser.find_elements(By.CSS_SELECTOR, "[data-testid='stBaseButton-primary']")
            if primary_btns:
                primary_btn = primary_btns[0]
                # Scroll into view
                browser.execute_script("arguments[0].scrollIntoView(true);", primary_btn)
                time.sleep(1)
                print(f"   Scrolled to primary button, visible={primary_btn.is_displayed()}")

        if primary_btn:
            print(f"\n[5] Clicking Add Card button...")
            # Use JavaScript click to avoid interception issues
            browser.execute_script("arguments[0].click();", primary_btn)
            print("   Clicked!")

            # Wait for save
            print("   Waiting for save...")
            time.sleep(5)

            # Check localStorage
            ls = browser.execute_script("return localStorage.getItem('churnpilot_cards')")
            if ls:
                cards = json.loads(ls)
                print(f"\n   *** SUCCESS! localStorage has {len(cards)} cards ***")
                if len(cards) > 0:
                    print(f"   Card: {cards[0].get('name')}")
            else:
                print("\n   localStorage is EMPTY after click")

                # Check for success message on page
                page_text = browser.find_element(By.TAG_NAME, "body").text
                if "Card added" in page_text or "Added:" in page_text:
                    print("   But found success message on page!")
                    # Maybe the save is delayed, wait more
                    time.sleep(5)
                    ls = browser.execute_script("return localStorage.getItem('churnpilot_cards')")
                    if ls:
                        cards = json.loads(ls)
                        print(f"   *** SUCCESS after longer wait! {len(cards)} cards ***")

        else:
            print("\n   ERROR: Could not find Add Card button!")
            browser.save_screenshot("debug_no_button.png")

            # Print page state
            body = browser.find_element(By.TAG_NAME, "body").text
            print(f"\n   Page content (first 800 chars):")
            print(f"   {body[:800]}")

        # Verify persistence with refresh
        print("\n[6] Refreshing to verify persistence...")
        browser.refresh()
        time.sleep(10)

        ls_after = browser.execute_script("return localStorage.getItem('churnpilot_cards')")
        if ls_after:
            cards = json.loads(ls_after)
            print(f"   After refresh: {len(cards)} cards persisted!")
            if len(cards) > 0:
                # Check dashboard shows the card
                body = browser.find_element(By.TAG_NAME, "body").text
                if "Total Cards" in body:
                    print("   Dashboard metrics visible!")
                    print("\n   *** TEST PASSED ***")
        else:
            print("   After refresh: localStorage is EMPTY")
            print("\n   *** TEST FAILED ***")

        browser.quit()

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()

        print("\n" + "-"*50)
        print("Relevant server logs:")
        for log in server_logs:
            if "save" in log.lower() or "Sync" in log or "Added" in log:
                print(f"   {log}")
        print("-"*50)
        print("Test completed.")


if __name__ == "__main__":
    run_test()
