from typing import Dict
import time

from ..gpio import GPIO

trigger_pin: int
echo_pin: int

SPEED_OF_LIGHT = 34300


def initialize(options: Dict):
    global trigger_pin, echo_pin
    trigger_pin = options["trigger_pin"]
    echo_pin = options["echo_pin"]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.output(trigger_pin, GPIO.LOW)
    # wait for sensor to settle
    time.sleep(2)


def get_distance():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)
    pulse_start = time.time()
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    return round(pulse_duration * (SPEED_OF_LIGHT / 2), 2)


def cleanup():
    GPIO.cleanup()
