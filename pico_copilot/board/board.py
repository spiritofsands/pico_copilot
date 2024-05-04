"""Board."""

from pico_copilot.utils.logger import LOG

from machine import Pin, PWM
from random import random


class Board:
    """Board hardware class."""
    DEFAULT_PWM_FREQ = 10000

    def __init__(self, config):
        """Board initialization."""
        self._config = config

        self._leds = {}
        for led_group, led_group_data in config['leds'].items():
            self._leds[led_group] = {}
            for led_name, led_config in led_group_data['leds'].items():
                if led_config['pin'] == 'LED':
                    self._leds[led_group][led_name] = Pin(
                        led_config['pin'], Pin.OUT)
                else:
                    self._leds[led_group][led_name] = PWM(
                        Pin(led_config['pin'], Pin.OUT))
                    self._leds[led_group][led_name].freq(self.DEFAULT_PWM_FREQ)

        # TBD: add
        # self.onboard_led = Pin("LED", Pin.OUT)

    def set_led_brightness(self, name, brightness):
        LOG.debug(f'HW set led brightness of {name} to {brightness}')

        for led_group_data in self._leds.values():
            if name in led_group_data:
                known_name = True
                if name == 'status':
                    if brightness > 0.5:
                        led_group_data[name].on()
                    else:
                        led_group_data[name].off()
                else:
                    led_group_data[name].duty_u16(
                        self._get_duty(brightness))
        if not known_name:
            LOG.warning('Unknown led name')

    def get_light_sensor(self):
        value = random()
        # LOG.debug(f'HW get light sensor: {value}')
        return value

    def get_button_state(self):
        return False

    def _get_duty(self, brightness):
        """Get duty value from 0.0-1.0 brightness range."""
        duty_max = 65535
        return round(duty_max * brightness)
