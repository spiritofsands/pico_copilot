"""Led module."""

from enum import Enum

from pico_copilot.utils.logger import LOG

class ButtonModule:
    """Button Module."""

    DELAY_BETWEEN_CLICKS_MIN = 0.01
    DELAY_BETWEEN_CLICKS_MAX = 0.2
    DELAY_LONG_CLICK = 2.0
    CLICK_MIN_DURATION = 0.01

    def __init__(self, board, state, name, tick_length):
        """Leds initialization."""
        self._board = board
        self._state = state
        self._name = name
        self._tick = tick_length

        self._pressed = False
        self._pressed_ticks = 0
        self._unpressed_ticks = 0

        self._previous_click = False
        self._just_released = False
        self._double_click_possible = False
        self._delay_ticks = 0

        self._long_click_possible = False
        self._single_click_possible = False
        self._click_handled = False
        self.events = []

        # Always hardcoded
        self.updates_available = True

    def update(self):
        button_pressed = self._board.get_button_state()
        self._check_button(button_pressed)

    def _check_button(self, event_pressed=True):
        if event_pressed:
            if self._pressed:
                # LOG.debug('Button kept pressed')
                self._pressed_ticks += 1

                # The only event handled before button release
                if self._is_long_click() and self._long_click_possible:
                    self._add_event('long_click')
                    self._long_click_possible = False
                    self._click_handled = True
            else:
                if self._just_released:
                    # LOG.debug('Button pressed second time')
                    self._double_click_possible = True
                else:
                    # LOG.debug('Button pressed first time')
                    self._long_click_possible = True

                self._pressed = True
                self._pressed_ticks = 1
                self._click_handled = False
        else:
            if self._pressed:
                # LOG.debug('Button released')

                # Double click is handled on release
                if self._is_click():
                    if self._double_click_possible:
                        self._add_event('double_click')
                        self._click_handled = True
                        self._double_click_possible = False
                        self._just_released = False
                    # Single click is handled after a delay
                    # to be able to process a double click

                    self._pressed = False

                    self._just_released = True
                    self._delay_ticks = 1
                else:
                    # LOG.debug('Click too short, ignoring')
                    self._click_handled = True

            else:
                # LOG.debug('Button kept unpressed')

                # Need to keep track of delay in case of double click
                if self._just_released:
                    self._delay_ticks += 1

                    if not self._is_double_click_delay():
                        self._just_released = False

                        if not self._click_handled and self._is_click():
                            self._add_event('single_click')
                            self._click_handled = True
                            self._pressed_ticks = 0

    def _pressed_time(self, time):
        return time * self._tick

    def _is_double_click_delay(self):
        return self._pressed_time(
            self._delay_ticks) <= self.DELAY_BETWEEN_CLICKS_MAX

    def _is_click(self):
        return self._pressed_time(
            self._pressed_ticks) >= self.CLICK_MIN_DURATION

    def _is_long_click(self):
        pressed_time = self._pressed_ticks * self._tick
        return pressed_time >= self.DELAY_LONG_CLICK

    def _add_event(self, event):
        LOG.info(f'Got event: {event}')

        self._state.add_button_event(self._name, event)

    def set_ninja_mode(self, _state):
        pass
