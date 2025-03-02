"""Sensor module."""

import asyncio

from pico_copilot.utils.logger import LOG


class SensorManager:
    """Module to control light sensor."""

    def __init__(self, board, state, name, tick_length):
        """Light sensor initialization."""

        self._board = board
        self._state = state
        self._name = name
        self._tick = tick_length
        self._update_interval = self._state.get_sensor_update_interval('light')
        self.updates_available = True

        self._reset_time()

    def _get_light_sensor(self):
        """Get light sensor value."""
        value = self._board.get_light_sensor()
        return value

    async def update(self):
        if not self.updates_available:
            return

        if self._time >= self._update_interval:
            self._state.set_sensor(self._name, self._get_light_sensor())
            self._reset_time()

        self._advance_time()

    def _advance_time(self):
        self._time += self._tick

    def _reset_time(self):
        self._time = 0

    def toggle(self, enabled):
        """Toggle the module."""
        self.updates_available = enabled
        LOG.info(f'Light sensor enabled: {enabled}')
