"""Led module."""

import asyncio

from pico_copilot.modules.animations.animation import (
    Animation,
)
from pico_copilot.utils.logger import LOG


class LedManager:
    """Module to control leds through PWM."""

    def __init__(self, board, state, name, tick_length):
        """Led initialization."""

        self._auto_brightness_modifier = 1.0
        self._hardware_brightness_modifier = 1.0

        self._board = board
        self._state = state
        self._name = name
        self._tick = tick_length
        self._hardware_brightness_modifier = (
            self._state.get_leds_hardware_brightness_modifier(self._name))
        leds = self._state.get_leds_brightness(self._name)
        self._led_names = leds.keys()
        self._set_led_brightness(leds)

        self.updates_available = False
        self._current_animation = None
        self._animation_mode = None

        self._animation = None

    def set_auto_brightness_modifier(self, brightness):
        """Set the auto brightness modifier."""
        if not 0.0 <= brightness <= 1.0:
            LOG.warning('Brightness modifier should be > 0 and < 1, got '
                        f'{brightness}')
            brightness = 1.0
        self._auto_brightness_modifier = brightness

    def set_all_leds_brightness(self, value):
        """Set all leds to a brightness."""
        leds = {
            led_name: {
                'brightness': value
            }
            for led_name in self._led_names
        }

        LOG.info(f'All LED brightness of {self._name} is set to: {value}')
        self._set_led_brightness(leds)

    def _set_led_brightness(self, leds):
        """Update leds params."""
        for name, params in leds.items():
            brightness = self._adjust_brightness(params['brightness'])
            current_brightness = self._state.get_leds_brightness(
                self._name)[name]['brightness']

            if current_brightness != brightness:
                # set the physical brightness
                self._board.change_brightness(name, brightness)
                # update the state to reflect the physical brightness
                self._state.set_led_brightness(self._name, name, brightness)

    def _adjust_brightness(self, brightness):
        """Adjust brightness taking the auto brightness into account."""
        if not (0.0 <= brightness <= 1.0):
            LOG.error(f'Brightness value is out of bounds: {brightness}')
            return

        brightness_value = (brightness * self._auto_brightness_modifier *
                            self._hardware_brightness_modifier)

        return brightness_value

    def set_animation(self, animation_name, animation_mode):
        """Play leds animation or disable it."""
        if not (animation_name and animation_mode):
            LOG.info(f'LED {self._name}: animation disabled')
            self.updates_available = False
            self._animation = None
            return

        self.updates_available = True
        self._current_animation = animation_name
        self._animation_mode = animation_mode
        self._animation = Animation(self._current_animation, self._tick)
        LOG.info(f'LED {self._name}: animation was set to '
                 f'{self._current_animation} ({self._animation_mode})')

    async def update(self):
        if not self.updates_available:
            return

        if self._animation:
            if not self._animation.finished:
                frame = self._animation.generate_frame()
                # LOG.debug(f'Got frame {frame}')

                leds = {
                    led_name: {
                        'brightness': led_brightness
                    }
                    for led_name,
                    led_brightness in zip(self._led_names,
                                          frame)
                }
                self._set_led_brightness(leds)
            else:
                if self._animation_mode == 'repeat':
                    # LOG.debug('Repeating animation '
                    #           f'"{self._current_animation}"')
                    self._animation.reset()
                    self._state.set_leds_animation_finished(self._name, False)

                else:
                    self.updates_available = False
                    LOG.debug('Animation finished')
                    self._state.set_leds_animation_finished(self._name, True)

    def toggle(self, enabled):
        """Toggle the module."""
        self.updates_available = enabled
        LOG.info(f'LED {self._name} enabled: {enabled}')
        if not enabled:
            self.set_all_leds_brightness(0.0)
