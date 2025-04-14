import network
import time
import machine
import os

from lib.config_manager import ConfigManager

cfg = ConfigManager()

def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='PresenceSensor_SETUP', password='setup1234')
    print('Access Point active:', ap.ifconfig())
    return ap

def try_connect_wifi(ssid, password, retries=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected() and retries > 0:
        time.sleep(1)
        retries -= 1
        print(f"Trying to connect... {retries}s left")

    if wlan.isconnected():
        print('Connected to WiFi:', wlan.ifconfig())
        return True
    else:
        print('Failed to connect to WiFi.')
        return False

def check_firmware_update(current_version):
    import urequests
    try:
        response = urequests.get('http://your-server-ip/latest_version.txt')
        if response.status_code == 200:
            latest_version = response.text.strip()

            if latest_version != current_version:
                print("Firmware update needed! Triggering OTA...")
                import lib.ota_updater as ota_updater
                ota_updater.download_and_install('http://your-server-ip/firmware_encrypted.bin')
                cfg.update_version(latest_version)
                machine.reset()
            else:
                print("Firmware is up to date.")
    except Exception as e:
        print("Version check error:", e)

def config_exists():
    try:
        with open('config.json') as f:
            return True
    except:
        return False

def main():
    if config_exists():
        print("Config.json found, attempting Wi-Fi connection...")
        cfg = ConfigManager()
        if try_connect_wifi(cfg.config['ssid'], cfg.config['password']):
            print("Wi-Fi connected, checking for firmware updates...")
            check_firmware_update(cfg.get_version())

            # Wi-Fi good, OTA check good, continue to main app
            import main as app_main
            app_main.main()
        else:
            print("Wi-Fi connection failed, starting setup AP...")
            import lib.webserver as webserver
            start_access_point()
            webserver.start_web_server()
    else:
        print("No config.json, starting setup AP...")
        import lib.webserver as webserver
        start_access_point()
        webserver.start_web_server()

if __name__ == "__main__":
    main()
