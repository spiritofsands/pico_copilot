"""State module."""

from pico_copilot.utils.logger import LOG


class State:
    """Module to control the state."""

    def __init__(self, state):
        """All modules initialization."""
        self._state = state.copy()
        self._max_brightness = 1

    def update(self, state):
        """Externally change the state."""
        self._state = state.copy()

    def get_leds_brightness(self, led_type):
        """Get leds brightness."""
        return self._state['leds'][led_type]['leds']

    def get_leds_state(self, led_type):
        """Get leds state like animation."""
        return self._state['leds'][led_type]['state']

    def set_led_brightness(self, led_type, led_name, brightness):
        """Set led brightness."""
        self._state['leds'][led_type]['leds'][led_name] = {
            'brightness': brightness
        }

    # TODO: refactor to more precise functions
    def set_leds_state(self, led_type, param, value):
        """Set leds state like animation."""
        self._state['leds'][led_type]['state'][param] = value

    def get_sensor(self, sensor_name):
        """Get sensor value."""
        return self._state['sensors'][sensor_name]['value']

    def get_sensor_update_interval(self, sensor_name):
        """Get sensor update interval."""
        return self._state['sensors'][sensor_name]['update_interval']

    def set_sensor(self, sensor_name, value):
        """Set sensor data."""
        self._state['sensors'][sensor_name]['value'] = value

    def get_button_events(self, button_name):
        """Get button states."""
        return self._state['buttons'][button_name].keys()

    def add_button_event(self, button_name, event):
        """Set.button event true"""
        self._state['buttons'][button_name][event] = True

    def retrieve_button_event(self, button_name, event):
        """Set.button event true"""
        hapenned = self._state['buttons'][button_name][event]
        if hapenned:
            self._state['buttons'][button_name][event] = False
        return hapenned

    def has_button_events(self, button_name):
        return any(value
                   for value in self._state['buttons'][button_name].values())

    # TODO: remove
    def get_events(self):
        return self._state['events']
