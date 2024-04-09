"""Board module."""

from typing import List


class PicoBoardModule:
    """Module to manage Raspberry Pico board."""

    class PWM:
        """Abstract PWM class."""

        def __init__(self, pin: int):
            """PWM initialization."""
            self.pin: int = pin
            self.value: int = 0
            # TODO

    class Button:
        """Abstract Button class."""

        def __init__(self, pin: int):
            """PWM initialization."""
            self.pin: int = pin
            self.pressed: bool = False
            # TODO

    def __init__(self):
        """Board initialization."""
        self._pwm_list: List[self.PWM] = []
        self._button_list: List[self.Button] = []

    def map_pwm(self, pin: int):
        """Map the pin number with PWM."""
        self._pwm_list.append(self.PWM(pin))

    def map_button(self, pin: int):
        """Map the pin number with a button."""
        self._button_list.append(self.Button(pin))

    # TODO: emit signal

    def status(self) -> List[str]:
        """List of strings with module status."""

        def _pwm_text():
            items = {
                pwm_item.pin: pwm_item.value for pwm_item in self._pwm_list
            }
            return f'PWM: {items}'

        def _button_text():
            items = {
                button_item.pin: button_item.pressed
                for button_item in self._button_list
            }
            return f'button: {items}'

        return [
            _pwm_text(),
            _button_text(),
        ]
