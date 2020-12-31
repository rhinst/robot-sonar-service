from typing import Dict
from himl import ConfigProcessor
from os import environ
import os.path


def get_config_path(env: str) -> str:
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + f"/../config/{env}")


def load_config(env: str = "dev") -> Dict:
    processor = ConfigProcessor()
    config_path = get_config_path(env)
    config = processor.process(path=config_path)

    config["logging"]["level"] = environ.get(
        "LOGGING_LEVEL", config["logging"]["level"]
    )
    config["logging"]["filename"] = environ.get(
        "LOGGING_FILENAME", config["logging"]["filename"]
    )
    config["redis"]["host"] = environ.get("REDIS_HOST", config["redis"]["host"])
    config["redis"]["port"] = int(environ.get("REDIS_PORT", config["redis"]["port"]))
    config["device"]["options"]["trigger_pin"] = int(
        environ.get("SONAR_TRIGGER_PIN", config["device"]["options"]["trigger_pin"])
    )
    config["device"]["options"]["echo_pin"] = int(
        environ.get("SONAR_ECHO_PIN", config["device"]["options"]["echo_pin"])
    )

    return config
