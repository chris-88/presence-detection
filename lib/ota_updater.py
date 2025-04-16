import urequests as requests
import time
import machine
import os

OTA_BASE_URL = "https://raw.githubusercontent.com/chris-88/presence-detection/ota-stub"
MANIFEST_URL = f"{OTA_BASE_URL}/manifest.txt"
VERSION_URL = f"{OTA_BASE_URL}/version.txt"

def get_current_version(cfg):
    return cfg.get_version()

def get_latest_version():
    try:
        r = requests.get(VERSION_URL)
        if r.status_code == 200:
            return r.text.strip()
    except Exception as e:
        print("❌ Failed to fetch version.txt:", e)
    return None

def update_available(cfg):
    current = get_current_version(cfg)
    latest = get_latest_version()
    print(f"🔁 OTA Version check: current={current}, latest={latest}")
    return latest and current != latest, latest

def fetch_and_write_file(path):
    try:
        url = f"{OTA_BASE_URL}/{path}"
        print(f"⬇️ Fetching: {url}")
        r = requests.get(url)
        if r.status_code == 200:
            dir_path = "/".join(path.split("/")[:-1])
            if dir_path and not dir_path in os.listdir():
                try:
                    os.mkdir(dir_path)
                except:
                    pass
            with open(path, "w") as f:
                f.write(r.text)
            print(f"✅ Updated {path}")
        else:
            print(f"⚠️ Failed to fetch {path}, status: {r.status_code}")
    except Exception as e:
        print(f"❌ Error fetching {path}:", e)

def perform_update(cfg, new_version):
    try:
        r = requests.get(MANIFEST_URL)
        if r.status_code != 200:
            print("❌ Failed to fetch manifest.")
            return

        files = [line.strip() for line in r.text.splitlines() if line.strip()]
        print("📦 Files to update:", files)

        for file in files:
            fetch_and_write_file(file)

        cfg.update_version(new_version)
        print("✅ OTA update complete. Rebooting...")
        time.sleep(2)
        machine.reset()

    except Exception as e:
        print("❌ OTA update failed:", e)
