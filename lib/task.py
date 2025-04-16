import time

class Task:
    def __init__(self, interval_ms):
        self.interval_ms = interval_ms
        self.last_run = time.ticks_ms()

    def should_run(self):
        now = time.ticks_ms()
        return time.ticks_diff(now, self.last_run) >= self.interval_ms

    def run(self):
        raise NotImplementedError("Task must implement run()")

    def update(self):
        if self.should_run():
            self.last_run = time.ticks_ms()
            self.run()