from machine import Pin
import time
from lib.task import Task

class PresenceTask(Task):
    def __init__(self, cfg, interval_ms=100):
        super().__init__(interval_ms)
        self.pir_pin = Pin(34, Pin.IN)

    def run(self):
        state = self.pir_pin.value()
        timestamp = time.time()
        if state:
            print(f"🟢 PIR: detected @ {timestamp}s")
        else:
            print(f"⚫ PIR: clear @ {timestamp}s")
