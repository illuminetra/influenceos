# ======================================================
#   Influence OS by Black Aqua India Pvt Ltd
# ======================================================

print("\n" + "="*60)
print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
print("="*60 + "\n\n")

import uiautomator2 as u2
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

# ------------------ Helper Function ------------------
def click_element(d, resourceId=None, text=None, description=None, retries=5, interval=1):
    """Click an element using resourceId, text, or description with retries."""
    for attempt in range(1, retries+1):
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
        except Exception:
            pass
        time.sleep(interval)
    return False


# ------------------ Orientation Lock ------------------
def lock_orientation(serial):
    """Disable auto-rotation and lock device in portrait mode."""
    try:
        subprocess.run(["adb", "-s", serial, "shell", "settings", "put", "system", "accelerometer_rotation", "0"])
        subprocess.run(["adb", "-s", serial, "shell", "settings", "put", "system", "user_rotation", "0"])
        subprocess.run("adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main", shell=True)
        print(f"[{serial}] 📱 Auto-Rotation disabled")
    except Exception as e:
        print(f"[{serial}] ⚠️ Failed to lock orientation: {e}")


# ------------------ Main Automation ------------------
def automate_device(serial):
    d = u2.connect(serial)
    print(f"\n🚀 Running Influence OS Script on {serial}")

    # Lock orientation first
    lock_orientation(serial)
    time.sleep(1)

    # Launch Chrome
    #d.app_start("com.android.chrome")
    #d.set_orientation("natural")
    print("✅ Opened Chrome")
    time.sleep(3)

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

    # Handle confirmation dialog
    if click_element(d, text="Close all tabs and groups"):
        print("✅ Closed all tabs and groups")
        time.sleep(1)

    # Go back to Chrome main page
    d.press("back")
    print("✅ Back to Home Screen")

    # Clear Chrome Storage & Cache
    d.shell('pm clear com.android.chrome')
    print("✅ Chrome storage and Cache Cleared Successfully!")

    # Completion banner
    print("\n" + "="*60)
    print(f"   {serial} - Script Completed Successfully!".center(60))
    print("="*60 + "\n")


# ------------------ Run on All Connected Devices ------------------
result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip() and "device" in line]

if not devices:
    print("⚠️ No connected devices found!")
else:
    print(f"📱 Found {len(devices)} device(s): {devices}")
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        executor.map(automate_device, devices)

print("\n" + "="*60)
print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
print("="*60 + "\n")
time.sleep(3)
