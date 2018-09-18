from bluepy.btle import Scanner
import paho.mqtt.publish as publish
import redis

import config

# publish.single(
#     payload='scan',
#     topic='{}/{}'.format(config.MQTT_TOPIC, 'status'),
#     hostname=config.MQTT_HOST,
#     port=config.MQTT_PORT
# )

# scan for ble devices
scanner = Scanner()
devices = scanner.scan(10.0)
ids = [dev.addr for dev in devices]

# get old ids from redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r_ids = r.get('ble:devices')
if not r_ids:
    r_ids = []
else:
    r_ids = r_ids.split(',')

# store new ids in redis
r.set('ble:devices', ','.join(ids))

added_ids = [id for id in ids if id not in r_ids]
deleted_ids = [id for id in r_ids if id not in ids]

if added_ids:
    # publish list of added ids
    msgs = [
        {'topic': '{}/{}'.format(config.MQTT_TOPIC, id), 'payload': 'on'}
        for id in added_ids
    ]
    publish.multiple(msgs, hostname=config.MQTT_HOST, port=config.MQTT_PORT)

if deleted_ids:
    # publish list of deleted ids
    msgs = [
        {'topic': '{}/{}'.format(config.MQTT_TOPIC, id), 'payload': 'off'}
        for id in deleted_ids
    ]
    publish.multiple(msgs, hostname=config.MQTT_HOST, port=config.MQTT_PORT)
