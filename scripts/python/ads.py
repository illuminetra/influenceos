import subprocess
import threading
import time
import re
import sys

# ======================================================
#   Influence OS by Black Aqua India Pvt Ltd
# ======================================================

print("\n" + "="*60)
print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
print("="*60 + "\n")

# Target URL
url = "https://www.bbc.co.uk/"

# Get connected devices
try:
    output = subprocess.check_output(["adb", "devices"], text=True)
except subprocess.CalledProcessError:
    print("❌ ADB not found or not responding.")
    sys.exit(1)

devices = [line.split()[0] for line in output.splitlines() if "\tdevice" in line]

if not devices:
    print("❌ No devices connected.")
    sys.exit(1)

print(f"Devices detected: {', '.join(devices)}")
print(f"Opening URL and scrolling simultaneously...\n")

threads = []

for device_id in devices:
    def device_thread(d=device_id):
        print(f"📱 Starting on {d}")

        # Open URL
        subprocess.run(["adb", "-s", d, "shell", "am", "start",
                        "-a", "android.intent.action.VIEW", "-d", url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(5)  # Wait for page to load

        # Get screen resolution
        try:
            out = subprocess.check_output(["adb", "-s", d, "shell", "wm", "size"], text=True)
            m = re.search(r"(\d+)x(\d+)", out)
            if m:
                width, height = int(m.group(1)), int(m.group(2))
            else:
                width, height = 1080, 1920
        except subprocess.CalledProcessError:
            width, height = 1080, 1920

        center_x = width // 2
        start_y = int(height * 0.80)
        end_y = int(height * 0.20)
        duration = "400"

        # Scroll down
        subprocess.run(["adb", "-s", d, "shell", "input", "swipe",
                        str(center_x), str(start_y), str(center_x), str(end_y), duration],
                       stdout=subprocess.DEVNULL)
        time.sleep(1.2)

        # Scroll up
        subprocess.run(["adb", "-s", d, "shell", "input", "swipe",
                        str(center_x), str(end_y), str(center_x), str(start_y), duration],
                       stdout=subprocess.DEVNULL)

        print(f"✅ {d} done scrolling")

    t = threading.Thread(target=device_thread)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n" + "="*60)
print("   Script Execution Completed Successfully!".center(60))
print("="*60)
print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
print("="*60 + "\n")
time.sleep(5)
