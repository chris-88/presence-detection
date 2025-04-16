import ujson
import network
import ubinascii
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(CONFIG_FILE) as f:
                config = ujson.load(f)
                print("Config loaded:", config)
                return config
        except Exception as e:
            print("Failed to load config: ", e)
            return None

    def exists(self):
        try:
            with open(CONFIG_FILE):
                return True
        except:
            return False

    def save_config(self, ssid, password, location):
        try:
            self.config = {
                "ssid": ssid,
                "password": password,
                "location": location,
                "firmware_version": "0.0.1"  # default initial version
            }
            with open(CONFIG_FILE, "w") as f:
                ujson.dump(self.config, f)
            print("Config saved.")
            return True
        except Exception as e:
            print("Failed to save config:", e)
            return False

    def clear_config(self):
        try:
            os.remove(CONFIG_FILE)
            print("Config cleared.")
            return True
        except Exception as e:
            print("Failed to clear config:", e)
            return False

    def generate_device_id(self):
        wlan = network.WLAN(network.STA_IF)
        mac = wlan.config("mac")
        mac_suffix = ubinascii.hexlify(mac[-3:]).decode()
        location = self.config["location"].replace(" ", "_").lower() if self.config and "location" in self.config else "unknown"
        return f"presence_sensor_{mac_suffix}_{location}"

    def get_version(self):
        if self.config and "firmware_version" in self.config:
            return self.config["firmware_version"]
        return "0.0.0"

    def update_version(self, new_version):
        if self.config:
            self.config["firmware_version"] = new_version
            with open(CONFIG_FILE, "w") as f:
                ujson.dump(self.config, f)
            print("Firmware version updated to", new_version)
