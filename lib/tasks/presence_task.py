from machine import Pin
import mqtt_client
from lib.task import Task

class PresenceTask(Task):
    def __init__(self, cfg, interval_ms=500):
        super().__init__(interval_ms)
        self.pir = Pin(34, Pin.IN)
        self.last_state = None
        self.cfg = cfg
        self.topics = cfg.get_mqtt_topics()

        mqtt_client.set_callback(self.mqtt_callback)
        mqtt_client.subscribe(b"home/presence/update")

    def mqtt_callback(self, topic, msg):
        if topic == b"home/presence/update" and msg == b"start":
            print("OTA update requested via MQTT.")
            import lib.ota_updater as ota_updater
            ota_updater.download_and_install('http://your-server-ip/firmware_encrypted.bin')

    def run(self):
        mqtt_client.check_msg()

        current_state = self.pir.value()

        if current_state != self.last_state:
            self.last_state = current_state

            if current_state:
                mqtt_client.publish(self.topics["presence_state_topic"], b"detected")
                print("Motion detected!")
            else:
                mqtt_client.publish(self.topics["presence_state_topic"], b"clear")
                print("No motion.")
