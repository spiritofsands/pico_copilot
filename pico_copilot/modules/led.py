"""Led module."""

from typing import List

from pico_copilot.modules.led_animations import (
    ANIMATIONS,
    Animation,
)
from pico_copilot.utils.logger import LOG


class LedManager:
    """Module to control leds through PWM."""

    def __init__(self, board, state, name, tick_length):
        """Led initialization."""

        self._brightness_cap = 1.0

        self._board = board
        self._state = state
        self._name = name
        self._tick = tick_length
        leds = self._state.get_leds_brightness(self._name)
        self._led_names = leds.keys()
        self._set_led_brightness(leds)

        self.updates_available = False
        self._current_animation = None
        self._animation_mode = None

        self._animation = None

        self._ninja_mode = False

    def set_brightness_cap(self, brightness):
        """Set the maxinum brightness value."""
        assert 0.0 <= brightness <= 1.0
        self._brightness_cap = brightness

    def set_all_leds_brightness(self, value):
        """Set all leds to max brightness."""
        leds = {led_name: {'brightness': value}
                for led_name in self._led_names}
        self._set_led_brightness(leds)

    def _set_led_brightness(self, leds):
        """Update leds params."""
        for name, params in leds.items():
            # LOG.debug(f'Changing {name} led brightness')
            brightness = self._adjust_brightness(params['brightness'])
            # set the physical brightness
            self._board.change_brightness(name, brightness)
            # update the state to reflect the physical brightness
            self._state.set_led_brightness(self._name,
                                           name, brightness)

    def _adjust_brightness(self, brightness):
        """Adjust brightness taking the max brightness into account."""
        assert 0.0 <= brightness <= 1.0
        return brightness * self._brightness_cap

    def set_animation(self, animation_name, animation_mode):
        """Play leds animation."""
        if animation_name not in ANIMATIONS:
            LOG.error(f'{animation_name} not in {ANIMATIONS.keys()}')
            return

        self.updates_available = True
        self._current_animation = animation_name
        self._animation_mode = animation_mode
        self._animation = Animation(self._current_animation, self._tick)

    def update(self):
        if self._animation or (self._ninja_mode and self._name == 'status'):
            if not self._animation.finished:
                frame = self._animation.generate_frame()
                # LOG.debug(f'Got frame {frame}')

                leds = {led_name: {'brightness': led_brightness}
                        for led_name, led_brightness in zip(
                            self._led_names, frame)}
                self._set_led_brightness(leds)
            else:
                if self._animation_mode == 'repeat':
                    # LOG.debug('Repeating animation '
                    #           f'"{self._current_animation}"')
                    self._animation.reset()
                else:
                    self.updates_available = False

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
