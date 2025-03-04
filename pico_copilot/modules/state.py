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

    def get_leds_hardware_brightness_modifier(self, led_type):
        """Get hardware_brightness_modifier leds state."""
        return self._state['leds'][led_type]['state'][
            'hardware_brightness_modifier']

    def get_leds_animation_playing(self, led_type):
        """Get animation playing leds state."""
        return self._state['leds'][led_type]['state']['animation_playing']

    def get_leds_animation_mode(self, led_type):
        """Get animation mode leds state."""
        return self._state['leds'][led_type]['state']['animation_mode']

    def get_leds_animation_finished(self, led_type):
        """Get animation finished leds state."""
        return self._state['leds'][led_type]['state']['animation_finished']

    def set_led_brightness(self, led_type, led_name, brightness):
        """Set led brightness."""
        self._state['leds'][led_type]['leds'][led_name] = {
            'brightness': brightness
        }

    def set_all_leds_brightness(self, led_type, brightness):
        """Set all leds brightness."""
        for value in self._state['leds'][led_type]['leds'].values():
            value['brightness'] = brightness

    def set_leds_animation_finished(self, led_type, value):
        """Set animation finished leds state."""
        self._state['leds'][led_type]['state']['animation_finished'] = value

    def set_leds_animation_playing(self, led_type, value):
        """Set a playing animation name leds state."""
        self._state['leds'][led_type]['state']['animation_playing'] = value

    def set_leds_animation_mode(self, led_type, value):
        """Set a playing animation mode leds state."""
        self._state['leds'][led_type]['state']['animation_mode'] = value

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
