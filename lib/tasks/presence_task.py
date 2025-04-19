from machine import Pin
import time
from lib.task import Task

class PresenceTask(Task):
    def __init__(self, cfg, interval_ms=100):
        super().__init__(interval_ms)
        self.pir_pin = Pin(2, Pin.IN)
        print("⏳ Waiting for PIR to stabilise...")
        time.sleep(5)  # Give PIR time to stabilise on boot
        print("✅ PIR ready.")

    def run(self):
        state = self.pir_pin.value()
        timestamp = time.time()
        if state == 1:
            print(f"🟢 PIR: detected @ {timestamp}s")
        else:
            print(f"⚫ PIR: clear @ {timestamp}s")
