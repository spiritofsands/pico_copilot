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
        self._hardware_brightness_modifier = self._state.get_leds_state(
            self._name)['hardware_brightness_modifier']
        leds = self._state.get_leds_brightness(self._name)
        self._led_names = leds.keys()
        self._set_led_brightness(leds)

        self.updates_available = False
        self._current_animation = None
        self._animation_mode = None

        self._animation = None

        self._ninja_mode = False

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
        self._set_led_brightness(leds)

    def _set_led_brightness(self, leds):
        """Update leds params."""
        for name, params in leds.items():
            # LOG.debug(f'Changing {name} led brightness to {params}')
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
        assert 0.0 <= brightness <= 1.0
        brightness_value = (brightness * self._auto_brightness_modifier *
                            self._hardware_brightness_modifier)
        return brightness_value

    def set_animation(self, animation_name, animation_mode):
        """Play leds animation or disable it."""
        if not (animation_name and animation_mode):
            self.updates_available = False
            return

        self.updates_available = True
        self._current_animation = animation_name
        self._animation_mode = animation_mode
        self._animation = Animation(self._current_animation, self._tick)

    async def update(self):
        if not self.updates_available:
            return

        if self._animation or (self._ninja_mode and self._name == 'status'):
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
                    self._state.set_leds_state(self._name,
                                               'animation_finished',
                                               False)

                else:
                    self.updates_available = False
                    self._state.set_leds_state(self._name,
                                               'animation_finished',
                                               True)

    def toggle(self, enabled):
        """Toggle the module."""
        self.updates_available = enabled
        LOG.info(f'LED {self._name} enabled: {enabled}')
        if not enabled:
            self.set_all_leds_brightness(0.0)

    def set_ninja_mode(self, state):
        self._ninja_mode = state

        if self._ninja_mode:
            if self._name == 'status':
                self.set_all_leds_brightness(0.5)
            else:
                self.set_all_leds_brightness(0.0)
                self.updates_available = False
        else:
            self.updates_available = True
