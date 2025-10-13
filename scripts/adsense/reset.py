# ======================================================
#   Influence OS by Black Aqua India Pvt Ltd
# ======================================================

import uiautomator2 as u2
import time
from concurrent.futures import ThreadPoolExecutor
import subprocess

# ------------------ Helper Function ------------------
def click_element(d, resourceId=None, text=None, description=None, retries=5, interval=1):
    """
    Tries to click an element using resourceId, text, or description.
    Retries `retries` times with `interval` seconds.
    Returns True if clicked, False if not found.
    """
    for attempt in range(1, retries + 1):
        try:
            if resourceId and d(resourceId=resourceId).exists:
                d(resourceId=resourceId).click()
                return True
            elif text and d(text=text).exists:
                d(text=text).click()
                return True
            elif description and d(description=description).exists:
                d(description=description).click()
                return True
        except:
            pass
        time.sleep(interval)
    return False

# ------------------ Main Script for a Device ------------------
def run_script_on_device(serial):
    try:
        d = u2.connect(serial)
        print("\n" + "="*60)
        print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
        print(f"Device: {serial}".center(60))
        print("="*60)

        # Launch Chrome
        d.app_start("com.android.chrome")
        print("✅ Opened Chrome")
        time.sleep(1)

        # Open tab switcher
        if click_element(d, description="Tabs") or click_element(d, resourceId="com.android.chrome:id/tab_switcher_button"):
            print("✅ Opened Tab Switcher")
            time.sleep(1)
        else:
            print("❌ Tab Switcher Button not found!")

        # Click "Close all tabs" if available
        if click_element(d, text="Close all tabs") or (click_element(d, resourceId="com.android.chrome:id/menu_button") and click_element(d, text="Close all tabs")):
            print("✅ Clicked 'Close all tabs'")
            time.sleep(1)
        else:
            print("❌ 'Close all tabs' option not found!")

        # Handle the confirmation dialog
        if click_element(d, text="Close all tabs and groups"):
            print("✅ Closed all tabs and groups")
            time.sleep(1)

        # Go back to Chrome main page
        d.press("back")
        print("✅ Back to Home Screen")

        # Clear Chrome Storage & Cache
        d.shell('pm clear com.android.chrome')
        print("✅ Chrome storage and Cache Cleared Successfully!")

        # Script Completion Branding
        print("\n" + "="*60)
        print("   Script Execution Completed Successfully!".center(60))
        print("="*60)
        print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
        print("="*60)
        time.sleep(2)

    except Exception as e:
        print(f"[{serial}] ❌ Error: {e}")

# ------------------ Get connected devices ------------------
def get_connected_devices():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = []
    for line in result.stdout.splitlines()[1:]:
        if line.strip() and "device" in line:
            devices.append(line.split()[0])
    return devices

# ------------------ Run on all devices concurrently ------------------
devices = get_connected_devices()
if not devices:
    print("❌ No devices connected.")
else:
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        executor.map(run_script_on_device, devices)
