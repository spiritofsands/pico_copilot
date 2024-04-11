"""Board."""


class Board:
    """Board hardware class."""

    def __init__(self, config):
        """Board initialization."""
        self._config = config

    def set_led_brightness(self, name, brightness):
        pass

    def get_light_sensor(self):
        pass

    def get_button_state(self):
        pass
