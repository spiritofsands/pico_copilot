"""Modes module."""

from pico_copilot.utils.logger import LOG


class Mode:
    """Mode business logic."""

    def __init__(self, state):
        self._state = state

        self.auto_brightness = None
        self.animation = {
            'tail': {
                'name': None,
                'mode': None,
            },
            'front': {
                'name': None,
                'mode': None,
            },
            'status': {
                'name': None,
                'mode': None,
            },
        }

        self.module_enabled = {
            'tail_leds': True,
            'front_leds': True,
            'status_leds': True,
            'sensors': True,
            'button1': True,
        }

        self.button_actions = {
            'single_click': '',
            'double_click': '',
            'long_click': '',
        }

    def check_events(self):
        return None


class StartupMode(Mode):
    """Startup mode."""

    def __init__(self, state):
        self._state = state

        LOG.info('Startup Mode')
        self.auto_brightness = True
        self.animation = {
            'tail': {
                'name': 'startup',
                'mode': 'once',
            },
            'front': {
                'name': 'startup',
                'mode': 'once',
            },
            'status': {
                'name': 'startup',
                'mode': 'once',
            },
        }

        self.module_enabled = {
            'tail_leds': True,
            'front_leds': True,
            'status_leds': True,
            'sensors': True,
            'button1': True,
        }

        self.button_actions = {
            'single_click': '',  # TBD
            'double_click': '',
            'long_click': 'poweroff',
        }

    def check_events(self):
        """Check for events and return a new state or None."""
        leds_finished_animation = (
            self._state.get_leds_state('tail')['animation_finished']
            and self._state.get_leds_state('front')['animation_finished'])

        if leds_finished_animation:
            return NormalMode(self._state)

        return None


class NormalMode(Mode):
    """Normal mode."""

    def __init__(self, state):
        self._state = state

        LOG.info('Normal Mode')
        self.auto_brightness = True
        self.animation = {
            'tail': {
                'name': 'normal',
                'mode': 'repeat',
            },
            'front': {
                'name': 'normal',
                'mode': 'repeat',
            },
            'status': {
                'name': 'normal',
                'mode': 'repeat',
            },
        }

        self.module_enabled = {
            'tail_leds': True,
            'front_leds': True,
            'status_leds': True,
            'sensors': True,
            'button1': True,
        }

        self.button_actions = {
            'single_click': '',  # TBD
            'double_click': 'toggle_brightness',
            'long_click': 'poweroff',
        }

    def check_events(self):
        return None


class PoweroffMode(Mode):
    """Poweroff mode."""

    def __init__(self, state):
        self._state = state

        LOG.info('Poweroff Mode')
        self.auto_brightness = False
        self.animation = {
            'tail': {
                'name': None,
                'mode': None,
            },
            'front': {
                'name': None,
                'mode': None,
            },
            'status': {
                'name': None,
                'mode': None,
            },
        }

        self.module_enabled = {
            'tail_leds': False,
            'front_leds': False,
            'status_leds': False,
            'sensors': False,
            'button1': True,
        }

        self.button_actions = {
            'single_click': '',
            'double_click': '',
            'long_click': 'startup',
        }
