import uiautomator2 as u2
import threading
import time
import random
import subprocess

# ======================================================
#   Influence OS by Black Aqua India Pvt Ltd
# ======================================================

URL = "https://crickettang.in/"
PAGE_KEYWORD = "Cricket Tang"   # text to verify page load
RETRIES = 10
DELAY = 2

# ------------------------------
# Get connected devices via ADB
# ------------------------------
def get_connected_devices():
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]  # skip header
    devices = [line.split("\t")[0] for line in lines if "device" in line]
    return devices

# ------------------------------
# Wait for webpage to load
# ------------------------------
def wait_for_page_load(d, keyword=PAGE_KEYWORD, retries=RETRIES, delay=DELAY):
    for attempt in range(1, retries + 1):
        if d(textContains=keyword).exists:
            print(f"✅ Webpage loaded successfully - [attempt {attempt}]")
            return True
        print(f"⏳ Waiting for webpage to load... [{attempt}/{retries}]")
        time.sleep(delay)
    print("❌ Webpage failed to load after max retries.")
    return False

# ------------------------------
# Perform random scrolls (10–20)
# ------------------------------
def random_scroll_behavior(d):
    scrolls = random.randint(5, 10)
    print(f"🌀 Performing {scrolls} random scrolls...")
    
    for i in range(scrolls):
        direction = random.choice(["up", "down"])
        width, height = d.window_size()
        start_x = width // 2
        start_y = int(height * 0.8)
        end_y = int(height * 0.2)

        if direction == "down":
            print(f"⬇️ Scrolling down ({i+1}/{scrolls})")
            d.swipe(start_x, start_y, start_x, end_y, 0.3)
        else:
            print(f"⬆️ Scrolling up ({i+1}/{scrolls})")
            d.swipe(start_x, end_y, start_x, start_y, 0.3)

        # random human-like delay between scrolls
        time.sleep(random.uniform(1.5, 3.5))

# ------------------------------
# Retry click helper
# ------------------------------
def click_with_retries(d, text=None, resourceId=None, description=None, retries=5, delay=1):
    for attempt in range(1, retries + 1):
        try:
            if text and d(text=text).exists:
                d(text=text).click()
                print(f"✅ Clicked element with text='{text}' [attempt {attempt}]")
                return True
            elif resourceId and d(resourceId=resourceId).exists:
                d(resourceId=resourceId).click()
                print(f"✅ Clicked element with resourceId='{resourceId}' [attempt {attempt}]")
                return True
            elif description and d(description=description).exists:
                d(description=description).click()
                print(f"✅ Clicked element with description='{description}' [attempt {attempt}]")
                return True
        except Exception as e:
            print(f"⚠️ Attempt {attempt}: click failed - {e}")
        time.sleep(delay)
    print(f"❌ Could not find element after {retries} retries.")
    return False

# ------------------------------
# Main per-device thread
# ------------------------------
def open_chrome_on_device(device):
    try:
        print(f"\n🚀 [{device}] Connecting via InfluenceOS...")
        d = u2.connect(device)

        print(f"🌐 [{device}] Launching Chrome with {URL}")
        d.shell(f'am start -a android.intent.action.VIEW -d "{URL}" com.android.chrome')
        time.sleep(3)

        if wait_for_page_load(d):
            print(f"✅ [{device}] Page loaded successfully — starting random browsing.")
            random_scroll_behavior(d)

            # Try clicking "Read Post"
            print(f"🖱️ [{device}] Attempting to click 'Read Post'...")
            if click_with_retries(d, text="Read Post", retries=8, delay=2):
                time.sleep(2)
                # After clicking, check if dismiss button appears
                print(f"🔍 [{device}] Checking for 'dismiss-button' popup...")
                click_with_retries(d, resourceId="dismiss-button", retries=5, delay=1)
        else:
            print(f"⚠️ [{device}] Page not fully loaded — skipping scroll & click.")
    except Exception as e:
        print(f"❌ [{device}] Error: {e}")

# ------------------------------
# Main execution
# ------------------------------
if __name__ == "__main__":
    print("=====================================================")
    print("   Influence OS by Black Aqua India Pvt Ltd")
    print("=====================================================")

    devices = get_connected_devices()

    if not devices:
        print("❌ No ADB devices found. Connect via USB/Wi-Fi first.")
        exit()

    print(f"📱 Connected Devices: {devices}")

    threads = []
    for device in devices:
        t = threading.Thread(target=open_chrome_on_device, args=(device,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n🎯 All device operations completed successfully.")
    print("=====================================================")
    print("   © Influence OS | Black Aqua India Pvt Ltd")
    print("=====================================================")
