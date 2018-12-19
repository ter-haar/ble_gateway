import paho.mqtt.client as mqtt
import config

mqtt = mqtt.Client()
mqtt.will_set("ble_gateway/status", "offline", retain=True)
mqtt.connect(
    host=config.MQTT_HOST,
    port=config.MQTT_PORT,
    keepalive=20,
    bind_address=""
)
mqtt.publish("ble_gateway/status", "online", retain=True)

mqtt.loop_forever()
