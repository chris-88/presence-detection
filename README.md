# Presence Sensor (Project GORK) v0.1

## Project Overview
GORK Presence Sensor is a production-grade, modular, scalable IoT presence detection device designed for Home Assistant integration via MQTT Auto-Discovery.

The system includes:
- Motion detection (PIR sensor)
- OTA firmware updates
- Captive Portal Wi-Fi Setup
- Soft recovery (fallback to AP mode if Wi-Fi fails)
- Dynamic MQTT topic generation based on MAC address and location
- Home Assistant auto-registration (no YAML required)

---

## File Structure
```
presence_sensor/ 
    ├── boot.py 
    ├── main.py 
    ├── README.md 
    ├── config.json (generated after setup) 
    ├── lib/ 
    │ ├── config_manager.py 
    │ ├── ota_updater.py 
    │ ├── task.py 
    │ └── webserver.py 
    └── lib/tasks/
     └── presence_task.py
```
---

## Development Environment Setup

**Device:** ESP32-WROOM-32  
**Firmware:** MicroPython v1.22.0 (or latest)  
**Dev Host:** Fedora Linux (or any modern Linux distro)  
**IDE:** Visual Studio Code + PlatformIO (optional) or Thonny/mpremote

### 1. Flash MicroPython
```bash
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 write_flash -z 0x1000 esp32-20240221-v1.22.0.bin
```

### 2. Install mpremote
```bash
pip install mpremote
```

### 3. Upload Files
```bash
mpremote connect /dev/ttyUSB0 fs cp boot.py :
mpremote connect /dev/ttyUSB0 fs cp main.py :
mpremote connect /dev/ttyUSB0 fs cp -r lib :
```

### 4. Running
```bash
mpremote connect /dev/ttyUSB0 repl
```

#### 4.a. Device will either:
- Start Wi-Fi captive portal for initial setup
- Connect to stored Wi-Fi and begin operation

#### 4.b. OTA Update Hosting
- Host latest_version.txt and firmware_encrypted.bin on a reachable HTTP server.
- Device checks version at every boot after Wi-Fi connection.

#### Config.json Example
```json
{
  "ssid": "HomeNetwork",
  "password": "supersecurepassword",
  "location": "living_room",
  "firmware_version": "0.0.1"
}
```
#### Known Limitations:
- No TLS on OTA downloads (planned)
- No encrypted MQTT (planned)
- No onboard temperature/humidity telemetry yet (planned)

62 Lower Labs © 2025