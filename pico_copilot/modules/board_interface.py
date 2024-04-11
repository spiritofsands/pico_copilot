"""Board abstraction interface."""


class BoardInterface:
    """Interface between an emulator window and a control module."""
    DEFAULT_BRIGHTNESS = 0.0

    def __init__(self, board, config):
        """Board initialization."""
        self._board = board

        for _set_name, set_params in config['leds'].items():
            for name, _params in set_params['leds'].items():
                self._board.set_led_brightness(
                    name, self.DEFAULT_BRIGHTNESS)

    def change_brightness(self, name, brightness):
        """Change brightness for a led element in the window."""
        # LOG.debug(f' Board IF: {name} brightness: {brightness}')
        self._board.set_led_brightness(name, brightness)

    def get_light_sensor(self):
        """Get the value of a light sensor slider in the window."""
        return self._board.get_light_sensor()

    def get_button_state(self):
        return self._board.get_button_state()
