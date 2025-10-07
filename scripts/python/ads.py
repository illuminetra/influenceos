import subprocess
import threading
import time
import re
import sys

# ======================================================
#   Influence OS by Black Aqua India Pvt Ltd
# ======================================================

def banner_start():
    print("\n" + "="*60)
    print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
    print("="*60 + "\n")

def banner_end():
    print("\n" + "="*60)
    print("   Script Execution Completed Successfully!".center(60))
    print("="*60)
    print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
    print("="*60 + "\n")

# ------------------------------------------------------
# ADB device utility functions
# ------------------------------------------------------

def get_connected_devices():
    """Return a list of connected device IDs via adb."""
    try:
        output = subprocess.check_output(["adb", "devices"], text=True)
    except subprocess.CalledProcessError:
        print("❌ ADB not found or not responding.")
        sys.exit(1)

    devices = [line.split()[0] for line in output.splitlines() if "\tdevice" in line]
    return devices

def get_screen_size(device_id):
    """Get screen width and height of a device."""
    try:
        out = subprocess.check_output(["adb", "-s", device_id, "shell", "wm", "size"], text=True)
        m = re.search(r"(\d+)x(\d+)", out)
        if m:
            return int(m.group(1)), int(m.group(2))
    except subprocess.CalledProcessError:
        pass
    return 1080, 1920  # fallback

# ------------------------------------------------------
# Device Action
# ------------------------------------------------------

def run_device_actions(device_id, url):
    """Open URL and perform scroll actions on a specific device."""
    print(f"📱 Starting on {device_id}")

    # Open URL
    subprocess.run(["adb", "-s", device_id, "shell", "am", "start",
                    "-a", "android.intent.action.VIEW", "-d", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(5)  # Wait for page to load

    # Get resolution
    width, height = get_screen_size(device_id)
    center_x = width // 2
    start_y = int(height * 0.80)
    end_y = int(height * 0.20)
    duration = "400"

    # Scroll down
    subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe",
                    str(center_x), str(start_y), str(center_x), str(end_y), duration],
                   stdout=subprocess.DEVNULL)
    time.sleep(1.2)

    # Scroll up
    subprocess.run(["adb", "-s", device_id, "shell", "input", "swipe",
                    str(center_x), str(end_y), str(center_x), str(start_y), duration],
                   stdout=subprocess.DEVNULL)

    print(f"✅ {device_id} done scrolling")

# ------------------------------------------------------
# Main Program
# ------------------------------------------------------

def main():
    banner_start()

    url = "https://www.bbc.co.uk/"  # target site

    devices = get_connected_devices()
    if not devices:
        print("❌ No devices connected.")
        return

    print(f"Devices detected: {', '.join(devices)}")
    print(f"Opening URL and scrolling simultaneously...\n")

    # Launch threads for all devices
    threads = []
    for device in devices:
        t = threading.Thread(target=run_device_actions, args=(device, url))
        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    banner_end()


if __name__ == "__main__":
    main()
