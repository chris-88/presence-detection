import time
from lib.config_manager import ConfigManager
from lib.tasks.presence_task import PresenceTask

def main():
    cfg = ConfigManager()

    tasks = [
        PresenceTask(cfg, interval_ms=500),
    ]

    print("🟢 GORK Live — Tasks Running")
    while True:
        for task in tasks:
            task.update()
        time.sleep(0.01)
