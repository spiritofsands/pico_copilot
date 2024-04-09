"""Sensor module."""

from typing import List

from pico_copilot.utils.logger import LOG


class SensorManager:
    """Module to control light sensor."""

    def __init__(self, board, state, name):
        """Light sensor initialization."""

        self._board = board
        self._state = state
        self._name = name
        # TBD: hardcoded
        self.updates_available = True
        self._ninja_mode = False

    def _get_light_sensor(self):
        """Get light sensor value."""
        value = self._board.get_light_sensor()
        return value

    def update(self):
        self._state.set_sensor(self._name, self._get_light_sensor())

    def set_ninja_mode(self, state):
        self._ninja_mode = state

        # Disable sensor on ninja mode
        self.updates_available = not self._ninja_mode
