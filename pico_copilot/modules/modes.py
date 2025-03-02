"""Modes module."""

from pico_copilot.utils.logger import LOG


class Mode:
    """Mode business logic."""

    def __init__(self, state):
        self._state = state

        self.leds = {
            'tail': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': None,
            },
            'front': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': None,
            },
            'status': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': None,
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

        self.leds = {
            'tail': {
                'animation': {
                    'name': 'startup',
                    'mode': 'once',
                },
                'brightness': None,
            },
            'front': {
                'animation': {
                    'name': 'startup',
                    'mode': 'once',
                },
                'brightness': None,
            },
            'status': {
                'animation': {
                    'name': 'startup',
                    'mode': 'once',
                },
                'brightness': None,
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

        self.leds = {
            'tail': {
                'animation': {
                    'name': 'normal',
                    'mode': 'repeat',
                },
                'brightness': None,
            },
            'front': {
                'animation': {
                    'name': 'normal',
                    'mode': 'repeat',
                },
                'brightness': None,
            },
            'status': {
                'animation': {
                    'name': 'normal',
                    'mode': 'repeat',
                },
                'brightness': None,
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
            'double_click': 'static',
            'long_click': 'poweroff',
        }

    def check_events(self):
        return None


class StaticMode(Mode):
    """Normal mode."""

    def __init__(self, state):
        self._state = state

        LOG.info('Static Mode')
        self.leds = {
            'tail': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': 0.5,
            },
            'front': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': 0.5,
            },
            'status': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': 0.5,
            },
        }

        self.module_enabled = {
            'tail_leds': True,
            'front_leds': True,
            'status_leds': True,
            'sensors': False,
            'button1': True,
        }

        self.button_actions = {
            'single_click': '',  # TBD
            'double_click': 'normal',
            'long_click': 'poweroff',
        }

    def check_events(self):
        return None


class PoweroffMode(Mode):
    """Poweroff mode."""

    def __init__(self, state):
        self._state = state

        LOG.info('Poweroff Mode')

        self.leds = {
            'tail': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': 0.0,
            },
            'front': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': 0.0,
            },
            'status': {
                'animation': {
                    'name': None,
                    'mode': None,
                },
                'brightness': 0.0,
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
