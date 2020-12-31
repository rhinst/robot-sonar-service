from unittest.mock import patch
import sonar.device.hcsro4 as device


def test_initialize():
    options = {"trigger_pin": 2, "echo_pin": 8}
    with patch("sonar.device.hcsro4.GPIO") as m_gpio, patch(
        "sonar.device.hcsro4.time.sleep"
    ):
        m_gpio.BCM = 123
        m_gpio.IN = 1
        m_gpio.OUT = 2
        m_gpio.HIGH = 0
        device.initialize(options)
        m_gpio.setmode.assert_called_once_with(m_gpio.BCM)
        m_gpio.setup.assert_any_call(options["trigger_pin"], m_gpio.OUT)
        m_gpio.setup.assert_any_call(options["echo_pin"], m_gpio.IN)
        m_gpio.output.assert_called_once_with(options["trigger_pin"], m_gpio.LOW)


def test_get_distance():
    device.trigger_pin = 1
    device.echo_pin = 2
    with patch("sonar.device.hcsro4.GPIO") as m_gpio, patch("sonar.device.hcsro4.time") as m_time:
        m_gpio.LOW = 0
        m_gpio.HIGH = 1
        m_gpio.input.side_effect = [m_gpio.LOW, m_gpio.HIGH, m_gpio.HIGH, m_gpio.LOW]
        m_time.time.side_effect = [1609423987.0, 1609423987.2, 1609423987.4, 1609423987.6]
        distance = device.get_distance()
    assert distance == 6860.0


def test_cleanup():
    with patch("sonar.device.hcsro4.GPIO") as m_gpio:
        device.cleanup()
        m_gpio.cleanup.assert_called_once()
