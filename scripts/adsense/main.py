import uiautomator2 as u2
import threading
import time
import random
import subprocess

# ======================================================
#   Influence OS by Black Aqua India Pvt Ltd
# ======================================================

URL = "https://crickettang.in/"
PAGE_KEYWORD = "Cricket Tang"
RETRIES = 10
DELAY = 2


def get_connected_devices():
    """Return list of connected ADB devices."""
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]
    devices = [line.split("\t")[0] for line in lines if "device" in line]
    return devices


def wait_for_page_load(d, keyword=PAGE_KEYWORD, retries=RETRIES, delay=DELAY):
    """Wait until the page containing `keyword` is loaded."""
    for attempt in range(1, retries + 1):
        if d(textContains=keyword).exists:
            print(f"✅ [{device}] Webpage loaded successfully - [attempt {attempt}]")
            return True
        print(f"⏳ [{device}] Waiting for webpage to load... [{attempt}/{retries}]")
        time.sleep(delay)
    print("❌ [{device}] Webpage failed to load after max retries.")
    return False


def random_scroll_behavior(d):
    """Perform random up/down scrolls (5–10 times)."""
    scrolls = random.randint(1, 10)
    print(f"🌀 [{device}] Performing {scrolls} random scrolls")
    
    width, height = d.window_size()
    start_x = width // 2
    start_y = int(height * 0.8)
    end_y = int(height * 0.2)

    for i in range(scrolls):
        direction = random.choice(["up", "down"])
        if direction == "down":
            d.swipe(start_x, start_y, start_x, end_y, 0.3)
        else:
            d.swipe(start_x, end_y, start_x, start_y, 0.3)
        time.sleep(random.uniform(1.5, 3.5))


def click_with_retries(d, text=None, resourceId=None, description=None, index=None, retries=5, delay=1):
    """Attempt to click element with retries."""
    for attempt in range(1, retries + 1):
        try:
            elements = None
            if text:
                elements = d(text=text)
            elif resourceId:
                elements = d(resourceId=resourceId)
            elif description:
                elements = d(description=description)

            if elements and len(elements) > 0:
                target = elements[index] if index is not None and index < len(elements) else elements[0]
                target.click()
                print(f"✅ [{device}] Clicked element [{text or resourceId or description}]")
                return True
        except Exception as e:
            print(f"⚠️ [{device}] Attempt {attempt}: click failed")
        time.sleep(delay)

    print(f"❌ [{device}] Could not find element after {retries} retries")
    return False


def human_scroll_and_misclick(d, ad_ids=None, max_scrolls=15, min_scrolls_before_click = random.randint(1, 5),
                              delay_range=(1.0, 3.0), click_chance=0.25, misclick_padding_fraction=0.15):
    """Scroll randomly and try to 'accidentally' click one of the ad elements."""
    if ad_ids is None:
        ad_ids = ["aswift_1_host", "aswift_2_host", "aswift_3_host", "aswift_4_host", "aswift_5_host", "aswift_6_host", "aswift_7_host", "aswift_8_host", "aswift_9_host"]

    width, height = d.window_size()
    start_x = width // 2
    top_y = int(height * 0.2)
    bottom_y = int(height * 0.8)

    print(f"🎯 [{device}] Searching for any Ad IDs")
    for scroll_num in range(1, max_scrolls + 1):
        # Random scroll
        direction = random.choice(["down", "up"])
        if direction == "down":
            d.swipe(start_x, bottom_y, start_x, top_y, random.uniform(0.25, 0.45))
        else:
            d.swipe(start_x, top_y, start_x, bottom_y, random.uniform(0.25, 0.45))
        time.sleep(random.uniform(*delay_range))

        if scroll_num < min_scrolls_before_click:
            continue

        # Check ads
        for ad_id in ad_ids:
            try:
                elems = d(resourceId=ad_id)
                if len(elems) == 0:
                    continue

                for elem in elems:
                    info = elem.info if hasattr(elem, 'info') else None
                    if not info:
                        continue

                    bounds = info.get("bounds") or info.get("visibleBounds") or info.get("frame")
                    if not bounds:
                        continue

                    left = bounds.get("left", bounds.get("x", 0))
                    top = bounds.get("top", bounds.get("y", 0))
                    right = bounds.get("right", left + bounds.get("width", 50))
                    bottom = bounds.get("bottom", top + bounds.get("height", 50))

                    ad_w = max(1, right - left)
                    ad_h = max(1, bottom - top)

                    roll = random.random()
                    if roll > click_chance:
                        print(f"🔎 [{device}] Found {ad_id} - Skipping this time")
                        continue

                    # Randomized click point
                    pad_x = int(ad_w * misclick_padding_fraction)
                    pad_y = int(ad_h * misclick_padding_fraction)
                    # compute click within bounds + small padding
                    click_x = random.randint(max(0, left - pad_x), min(width - 1, right + pad_x))
                    click_y = random.randint(max(0, top - pad_y), min(height - 1, bottom + pad_y))
                    # small jitter
                    click_x = max(0, min(width - 1, click_x + random.randint(-3, 3)))
                    click_y = max(0, min(height - 1, click_y + random.randint(-3, 3)))

                    try:
                        d.click(click_x, click_y)
                        print(f"✅ [{device}] Clicked Ad {ad_id} on scroll {scroll_num}")
                        return True
                    except Exception as e:
                        print(f"⚠️ [{device}] Failed to click {ad_id}: {e}")

            except Exception as e:
                print(f"⚠️ [{device}] Error checking ad '{ad_id}': {e}")

        time.sleep(random.uniform(0.5, 1.5))

    print("❌ [{device}] No Ad Click Performed After All Scrolls.")
    return False




def open_ip_rotation_url(d, file_path="/sdcard/Download/rotation_url.txt"):
    """Reads a URL from /sdcard/Download/rotation_url.txt on the Android device and opens it in Chrome browser."""
    try:
        # Read file content using ADB shell command
        content = d.shell(f"cat {file_path}").output.strip()
        url = content.strip()
        print(f"📡 [{device}] Rotating IP with URL: {url}")
        if not url:
            print(f"⚠️ No URL found in {file_path}")
            return False
        # Launch Chrome with the URL
        d.shell(f'am start -a android.intent.action.VIEW -d "{url}" com.android.chrome')
    except Exception as e:
        print(f"❌ Error opening URL: {e}")
        return False




def restart_socksdroid(d, retries=5, delay=2):
    """-stop and restart SocksDroid, then toggle its switch button.Automatically retries if it fails."""
    for attempt in range(1, retries + 1):
        try:
            # Force stop and relaunch
            d.shell("am force-stop net.typeblog.socks")
            time.sleep(1)
            
            open_ip_rotation_url(d)
            time.sleep(random.uniform(10, 30))
            
            d.shell("am start -n net.typeblog.socks/.MainActivity")
            time.sleep(2)
            # Try clicking the toggle button
            switch_action_button_btn = d(resourceId="net.typeblog.socks:id/switch_action_button")
            if switch_action_button_btn.exists:
                switch_action_button_btn.click()
                return True
            else:
                print("⚠️ Switch button not found, retrying...")
        except Exception as e:
            print(f"❌ Error during attempt {attempt}: {e}")
        # Wait before next retry
        time.sleep(delay)
    print("❌ Failed to restart SocksDroid after all retries.")
    return False




def open_chrome_on_device(device):
    """Main per-device workflow."""
    try:
        print(f"\n🚀 [{device}] Connecting via InfluenceOS...")
        d = u2.connect(device)

        print(f"🌐 [{device}] Launching Chrome with {URL}")
        d.shell(f'am start -a android.intent.action.VIEW -d "{URL}" com.android.chrome'); time.sleep(5); [click_with_retries(d, text=txt, retries=3, delay=1) for txt in ["Use without an account", "No, thanks"]]
        time.sleep(1)

        if wait_for_page_load(d):
            random_scroll_behavior(d)

            # Click "Read Post"
            if click_with_retries(d, text="Read Post", index=1, retries=5, delay=2):
                time.sleep(3)
                click_with_retries(d, resourceId="dismiss-button", retries=5, delay=1)

                if wait_for_page_load(d):
                    clicked = human_scroll_and_misclick(d)
                    if clicked:
                        print(f"🎯 [{device}] Ad clicked successfully!")
                        time.sleep(random.uniform(1, 30))

                        # Processing with IP Rotation
                        #open_ip_rotation_url(d)
                        #time.sleep(random.uniform(1, 30))
                        
                        # Restart SocksDroid
                        restart_socksdroid(d)
                        time.sleep(random.uniform(1, 30))

                        # Clear Chrome Storage & Cache
                        d.shell('pm clear com.android.chrome')
                        time.sleep(random.uniform(1, 10))
                        
                        # Restarting Script
                        open_chrome_on_device(device)
                    else:
                        print(f"⚠️ [{device}] No ad found after scrolling.")

                        # Processing with IP Rotation
                        #open_ip_rotation_url(d)
                        #time.sleep(random.uniform(1, 30))
                        
                        # Restart SocksDroid
                        restart_socksdroid(d)
                        time.sleep(random.uniform(1, 30))
                        
                        # Clear Chrome Storage & Cache
                        d.shell('pm clear com.android.chrome')
                        time.sleep(random.uniform(1, 10))
                        
                        # Restarting Script
                        open_chrome_on_device(device)
            else:
                print(f"🔁 [{device}] 'Read Post' not found — restarting operation.")
                open_chrome_on_device(device)
        else:
            print(f"⚠️ [{device}] Page not fully loaded — skipping scroll & click.")
    except Exception as e:
        print(f"❌ [{device}] Error: {e}")


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
