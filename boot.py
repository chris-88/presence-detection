import network
import time
import machine
from lib import config_manager, ota_updater

cfg = config_manager.ConfigManager()

def try_connect_wifi(ssid, password, retries=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected() and retries > 0:
        print(f"Trying to connect... {retries}s left")
        time.sleep(1)
        retries -= 1

    return wlan.isconnected()

def main():
    print("Config.json found, attempting Wi-Fi connection...")

    if cfg.config and try_connect_wifi(cfg.config["ssid"], cfg.config["password"]):
        print("Wi-Fi connected. Checking for OTA update...")
        needs_update, latest_version = ota_updater.update_available(cfg)
        if needs_update:
            print("🚀 New firmware available. Performing OTA...")
            ota_updater.perform_update(cfg, latest_version)
            return
        print("✔️ Firmware is up to date. Booting main...")
        try:
            import main as app_main
            app_main.main()
        except Exception as e:
            print("❌ Main app crashed:", e)
    else:
        print("❌ Wi-Fi connection failed. Rebooting into recovery...")
        time.sleep(2)
        machine.reset()

if __name__ == "__main__":
    main()
