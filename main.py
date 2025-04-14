import time
from lib.config_manager import ConfigManager
from lib.tasks.presence_task import PresenceTask

def main():
    cfg = ConfigManager()

    topics = cfg.get_mqtt_topics()

    # Initialize tasks
    tasks = [
        PresenceTask(cfg, interval_ms=500),
    ]

    # Main event loop
    while True:
        for task in tasks:
            task.update()
        time.sleep(0.01)
