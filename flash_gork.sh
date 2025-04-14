#!/bin/bash

# GORK Presence Sensor Deployment Tool
# by 62 Lower Labs

set -e  # Exit immediately if any command fails

# Constants
PORT=$(ls /dev/ttyUSB* 2>/dev/null | head -n 1)
FIRMWARE="ESP32_GENERIC-20241129-v1.24.1.bin"
BAUD=460800
PROJECT_FILES=(lib main.py boot.py)
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error trap
trap 'echo -e "${RED}💥 An unexpected error occurred. Exiting.${NC}"' ERR

# Helpers
section() {
  echo -e "${YELLOW}\n====================================="
  echo -e " $1"
  echo -e "=====================================${NC}"
}

success() {
  echo -e "${GREEN}✅ $1${NC}"
}

info() {
  echo -e "${YELLOW}➜ $1${NC}"
}

error_exit() {
  echo -e "${RED}❌ $1${NC}"
  exit 1
}

sleep_with_dots() {
  duration=$1
  interval=1
  elapsed=0
  echo -n "${YELLOW}Waiting"
  while [ $elapsed -lt $duration ]; do
    echo -n "."
    sleep $interval
    elapsed=$((elapsed + interval))
  done
  echo -e "${NC}"
}

# Start
START_TIME=$(date +%s)
section "GORK Presence Sensor Flash Tool"

# Check device
if [ -z "$PORT" ]; then
  error_exit "No ESP32 device detected on /dev/ttyUSB*"
fi
success "Found ESP32 device at $PORT"

# Check firmware
if [ ! -f "$FIRMWARE" ]; then
  error_exit "Firmware file not found: $FIRMWARE"
fi
success "Firmware file found: $FIRMWARE"

# Optional backup
read -p "Backup existing ESP32 filesystem before flashing? (y/n) " backup_files

if [ "$backup_files" == "y" ]; then
  mkdir -p $BACKUP_DIR
  info "Backing up files to $BACKUP_DIR ..."
  mpremote connect $PORT fs cp : "$BACKUP_DIR/"
  success "Backup complete."
fi

# Optional firmware flash
read -p "Erase flash and write MicroPython firmware? (y/n) " flash_firmware

if [ "$flash_firmware" == "y" ]; then
  section "Erasing Flash"
  esptool.py --chip esp32 --port $PORT erase_flash
  success "Flash erase complete."

  section "Flashing MicroPython Firmware"
  esptool.py --chip esp32 --port $PORT --baud $BAUD write_flash -z 0x1000 $FIRMWARE
  success "Firmware flashed successfully."

  info "Waiting for device to reboot and settle..."
  sleep_with_dots 5

  # Re-detect port in case port changes
  PORT=$(ls /dev/ttyUSB* 2>/dev/null | head -n 1)
  success "Re-detected ESP32 device at $PORT"
else
  info "Skipping firmware flashing."
fi

# Upload project files
section "Uploading Project Files"
for file in "${PROJECT_FILES[@]}"; do
  if [ -e "$file" ]; then
    info "Uploading $file..."
    mpremote connect $PORT fs cp -r $file :
    success "Uploaded $file"
  else
    error_exit "Project file missing: $file"
  fi
done

# Reset device
section "Resetting Device"
{ mpremote connect $PORT reset > /dev/null 2>&1 || true; }
success "Device reset command sent. Device may now be busy starting Wi-Fi setup."

# Done
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

section "🎉 GORK Flash Complete! 🚀 Device is Ready!"
info "Total operation time: ${ELAPSED} seconds."
