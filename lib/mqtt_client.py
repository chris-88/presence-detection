# Placeholder for MQTT client logic

class MQTTClient:
    def __init__(self, *args, **kwargs):
        pass

    def connect(self):
        print("Mock MQTT connect")

    def publish(self, topic, message):
        print(f"Mock publish: {topic} -> {message}")

    def disconnect(self):
        print("Mock MQTT disconnect")
