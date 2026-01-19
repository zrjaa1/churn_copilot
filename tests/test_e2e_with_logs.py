"""
E2E Test that captures Streamlit server logs to debug data loading.
"""

import subprocess
import sys
import time
import json
import os
import threading
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def run_test():
    """Run the test and capture server logs."""
    print("\n" + "="*60)
    print("E2E Test with Server Log Capture")
    print("="*60 + "\n")

    env = os.environ.copy()
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["PYTHONUNBUFFERED"] = "1"  # Don't buffer output

    # Start Streamlit with output capture
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

    # Collect logs in background
    logs = []
    def read_logs():
        for line in process.stdout:
            logs.append(line.strip())
            if "[ChurnPilot]" in line:
                print(f"  SERVER: {line.strip()}")

    log_thread = threading.Thread(target=read_logs, daemon=True)
    log_thread.start()

    print("Starting Streamlit app...")
    time.sleep(5)

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)

        url = "http://localhost:8599"

        # Step 1: Load page
        print("\n[Step 1] Loading page...")
        browser.get(url)
        time.sleep(8)

        # Step 2: Set test data
        print("\n[Step 2] Setting test data in localStorage...")
        test_card = {
            "id": "test-e2e-001",
            "name": "E2E Test Card",
            "issuer": "Test Bank",
            "annual_fee": 100,
            "credits": [],
            "created_at": "2024-01-01T00:00:00"
        }
        browser.execute_script(
            f"localStorage.setItem('churnpilot_cards', '{json.dumps([test_card])}')"
        )

        verify = browser.execute_script("return localStorage.getItem('churnpilot_cards')")
        print(f"   localStorage: {verify[:60]}...")

        # Step 3: Refresh and watch server logs
        print("\n[Step 3] Refreshing page and watching server logs...")
        browser.refresh()
        time.sleep(10)

        # Check localStorage
        after = browser.execute_script("return localStorage.getItem('churnpilot_cards')")
        print(f"   localStorage after refresh: {after[:60] if after else 'None'}...")

        # Check if card appears
        # Note: get_display_name strips "Card" from name, so look for "E2E Test"
        page_text = browser.page_source
        if "E2E Test" in page_text:
            print("   Card appears in UI: YES - Found 'E2E Test'")
        else:
            print("   Card appears in UI: NO")
            # Check sidebar content
            if "No cards tracked" in page_text:
                print("   Sidebar says: 'No cards tracked'")
            if "Library: 18 templates" in page_text:
                print("   Sidebar shows library template count")
            # Look for partial card data
            if "test-e2e-001" in page_text:
                print("   Card ID found in page!")
            if "Test Bank" in page_text:
                print("   Card issuer found in page!")

        # More refreshes
        for i in range(3):
            print(f"\n[Step 4.{i+1}] Additional refresh #{i+1}...")
            browser.refresh()
            time.sleep(8)

            after = browser.execute_script("return localStorage.getItem('churnpilot_cards')")
            print(f"   localStorage: {after[:60] if after else 'None'}...")

            if "E2E Test" in browser.page_source:
                print("   Card appears in UI: YES - SUCCESS!")
                break
            else:
                print("   Card appears in UI: NO")

        # Print relevant server logs
        print("\n" + "="*60)
        print("Server Logs (ChurnPilot):")
        print("="*60)
        churnpilot_logs = [l for l in logs if "ChurnPilot" in l]
        for log in churnpilot_logs:
            print(f"  {log}")

        if not churnpilot_logs:
            print("  (No ChurnPilot logs found)")

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
        print("\nApp stopped.")


if __name__ == "__main__":
    run_test()
