import subprocess
import sys
import importlib

# ======================================================
#   Influence OS by Black Aqua India Pvt Ltd
#   Python Environment Setup for uiautomator2
# ======================================================

REQUIRED_LIBRARIES = [
    "setuptools",
    "wheel",
    "pip",
    "uiautomator2",
    "adbutils",
    "requests",
    "urllib3",
    "six",
    "certifi",
    "idna",
    "chardet",
    "pure-python-adb",
    "progress",
    "psutil",
    "Pillow"
]

def install_package(package):
    """Install or upgrade a Python package using pip"""
    try:
        print(f"📦 Installing: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
        print(f"✅ Successfully installed: {package}")
    except Exception as e:
        print(f"❌ Failed to install {package}: {e}")

def main():
    print("\n" + "="*60)
    print("   Influence OS — Automated Python Setup".center(60))
    print("="*60 + "\n")

    # Step 1: Upgrade pip
    print("🚀 Upgrading pip to latest version...\n")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)

    # Step 2: Install all required libraries
    for lib in REQUIRED_LIBRARIES:
        install_package(lib)

    # Step 3: Verify installation
    print("\n🔍 Verifying installations...\n")
    for lib in REQUIRED_LIBRARIES:
        try:
            importlib.import_module(lib.split("==")[0])
            print(f"✅ {lib} is ready to use.")
        except ImportError:
            print(f"⚠️ {lib} not found even after installation!")

    print("\n" + "="*60)
    print("🎯 Environment Setup Completed Successfully!")
    print("   Influence OS by Black Aqua India Pvt Ltd".center(60))
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
