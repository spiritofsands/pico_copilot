"""Light Sensor module."""

# from pico_copilot.utils.logger import LOG

from machine import I2C, Pin

from bh1750 import BH1750


class LightSensor:
    """Light sensor abastraction."""

    def __init__(self, config):
        """Board initialization."""
        i2c = I2C(config['sensors']['light']['i2c'],
                  sda=Pin(config['sensors']['light']['sda']),
                  scl=Pin(config['sensors']['light']['scl']))

        self._bh1750 = BH1750(
            config['sensors']['light']['device_address'], i2c)

    def get_data(self):
        """Return real sensor measurements."""
        return self._bh1750.measurement
