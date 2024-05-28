"""Board."""

from pico_copilot.utils.logger import LOG
from pico_copilot.board.light_sensor import LightSensor

from machine import Pin, PWM


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

        self._light_sensor = LightSensor(self._config)

        # TBD: add
        # self.onboard_led = Pin("LED", Pin.OUT)

    def set_led_brightness(self, name, brightness):
        if name == 'status':
            LOG.debug(f'HW set led brightness of {name} to {brightness}')

        for led_group_data in self._leds.values():
            if name in led_group_data:
                known_name = True
                led_group_data[name].duty_u16(
                    self._get_duty(brightness))
        if not known_name:
            LOG.warning('Unknown led name')

    def get_light_sensor(self):
        """Return brightness from 0.0 to 1.0."""
        sensor_data = self._light_sensor.get_data()
        max_lux = 10000
        # linear here
        sensor_data = min(max_lux, sensor_data)
        value = sensor_data / max_lux
        LOG.debug(f'Calculated brightness value: {value} (from {sensor_data})')
        return value

    def get_button_state(self):
        return False

    def _get_duty(self, brightness):
        """Get duty value from 0.0-1.0 brightness range."""
        duty_max = 65535
        return round(duty_max * brightness)
