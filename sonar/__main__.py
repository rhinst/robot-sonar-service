import os
from itertools import cycle
from time import sleep
from typing import Dict

from redis import Redis

from sonar.config import load_config
import sonar.device

environment: str = os.getenv("ENVIRONMENT", "dev")
config: Dict = load_config(environment)
redis_client: Redis = Redis(host=config["redis"]["host"], port=int(config["redis"]["port"]))

sonar.device.initialize(config["device"]["name"], config["device"]["options"])
while cycle([True]):
    try:
        measurement = sonar.device.get_distance()
        redis_client.publish("subsystem.sonar.measurement", measurement)
        sleep(0.25)
    finally:
        redis_client.close()
        sonar.device.cleanup()