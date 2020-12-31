import os
from itertools import cycle
from time import sleep
from typing import Dict
from json import dumps

from redis import Redis
from redis.client import PubSub

from sonar.config import load_config
import sonar.device

environment: str = os.getenv("ENVIRONMENT", "dev")
config: Dict = load_config(environment)
redis: Redis = Redis(host=config["redis"]["host"], port=int(config["redis"]["port"]))
pubsub: PubSub = redis.pubsub()

sonar.device.initialize(config["device"]["name"], config["device"]["options"])
while cycle([True]):
    try:
        measurement = sonar.device.get_distance()
        message = {
            "type": "measurement",
            "data": measurement
        }
        redis.publish("subsystem.sonar", dumps(message))
        sleep(0.25)
    finally:
        pubsub.close()
        redis.close()
        sonar.device.cleanup()