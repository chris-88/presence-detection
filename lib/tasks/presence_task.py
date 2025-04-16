from machine import Pin
from lib.task import Task

class PresenceTask(Task):
    def __init__(self, cfg, interval_ms=500):
        super().__init__(interval_ms)
        self.pir_pin = Pin(34, Pin.IN)
        self.state = None

    def run(self):
        current_state = self.pir_pin.value()
        if current_state != self.state:
            self.state = current_state
            if self.state:
                print("🔔 PIR: detected")
            else:
                print("🌑 PIR: clear")
