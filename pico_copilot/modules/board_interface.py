"""Board abstraction interface."""


class BoardInterface:
    """Module to provide the interface of a board."""

    def __init__(self, config):
        """Board initialization."""
        self._leds = config['leds']
        self._config_updated = True

    def change_brightness(self, led_name, brightness):
        """Change brightness for a led."""
        self._leds[led_name] = brightness
        self._config_updated = True
