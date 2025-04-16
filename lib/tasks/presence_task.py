from machine import Pin
import time
from lib.task import Task

class PresenceTask(Task):
    def __init__(self, cfg, interval_ms=100):
        super().__init__(interval_ms)
        self.pir_pin = Pin(34, Pin.IN)
        self.state = self.pir_pin.value()

    def run(self):
        new_state = self.pir_pin.value()
        if new_state != self.state:
            self.state = new_state
            timestamp = time.time()
            if self.state:
                print(f"🟢 Motion detected @ {timestamp}s")
            else:
                print(f"⚫ Motion cleared @ {timestamp}s")
