import os
from itertools import cycle
from time import sleep
from typing import Dict

from redis import Redis

from sonar.config import load_config
from sonar.logging import logger, initialize_logger
import sonar.device


def main():
    environment: str = os.getenv("ENVIRONMENT", "dev")
    config: Dict = load_config(environment)
    initialize_logger(config["logging"]["level"], config["logging"]["filename"])
    redis_host = config["redis"]["host"]
    redis_port = config["redis"]["port"]
    logger.debug(f"Connecting to redis at {redis_host}:{redis_port}")
    redis_client: Redis = Redis(host=redis_host, port=redis_port)

    sonar.device.initialize(config["device"]["name"], config["device"]["options"])
    while cycle([True]):
        try:
            measurement = sonar.device.get_distance()
            redis_client.publish("subsystem.sonar.measurement", measurement)
            sleep(0.25)
        finally:
            redis_client.close()
            sonar.device.cleanup()


if __name__ == "__main__":
    main()
