"""Main entrance point."""


import sys
from os.path import abspath, dirname
from threading import Thread
from time import sleep
from copy import deepcopy

PACKAGE_DIR = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0, PACKAGE_DIR)

from emulator import Emulator
from pico_copilot.modules.control import ControlModule
from pico_copilot.modules.board_interface import BoardInterface

BOARD_CONFIG = {
    'leds':
    {
        'tail': {
            'leds': {
                'tail_bars': {'pin': 1},
                'top_v': {'pin': 2},
                'mid_v': {'pin': 3},
                'low_x': {'pin': 4},
            }
        },
        'front': {
            'leds': {
                'front_bars': {'pin': 5},
                'segment_edge': {'pin': 6},
                'segment_mid': {'pin': 7},
                'segment_center': {'pin': 8},
            }
        },
        'status': {
            'leds': {
                'status': {
                    'pin': 9},
            }
        }
    },
    'sensors':
    {
        'light': {'pin': 10},
    },
}


def generate_default_state():
    default_brightness = 0.5
    return {
        'leds':
        {
            'tail': {
                'state': {
                    'animation_playing': None,
                    'animation_mode': 'once',
                },
                'leds': {
                    'tail_bars': {'brightness': default_brightness},
                    'top_v': {'brightness': 0},
                    'mid_v': {'brightness': 0},
                    'low_x': {'brightness': 0},
                }
            },
            'front': {
                'state': {
                    'animation_playing': None,
                    'animation_mode': 'once',
                },
                'leds': {
                    'front_bars': {'brightness': default_brightness},
                    'segment_edge': {'brightness': 0},
                    'segment_mid': {'brightness': 0},
                    'segment_center': {'brightness': 0},
                }
            },
            'status': {
                'state': {
                    'animation_playing': None,
                    'animation_mode': 'once',
                },
                'leds': {
                    'status': {'brightness': default_brightness},
                }
            }
        },
        'sensors':
        {
            'light':
            {
                'value': default_brightness,
            },
        },
        'buttons':
        {
            'button1':
            {
                'single_click': False,
                'double_click': False,
                'long_click': False,
            },
        },
        'events':  # move to RO config?
        {
            'single_click': '',  # TBD
            'double_click': 'toggle_brightness',
            'long_click': 'ninja_mode',
        }
    }


def modify_state(original_state, animated=False, single_click=False):
    """Generate config for the system."""
    state = deepcopy(original_state)
    if animated:
        for group in state['leds']:
            state['leds'][group]['state']['animation_mode'] = 'repeat'

        state['leds']['front']['state']['animation_playing'] = 'startup'
        state['leds']['tail']['state']['animation_playing'] = 'startup'
        state['leds']['status']['state'][
            'animation_playing'] = 'slow_heartbeat'

    if single_click:
        state['buttons']['button1']['single_click'] = True

    return state


EMULATOR = Emulator()
BOARD = BoardInterface(EMULATOR, BOARD_CONFIG)
STATE = generate_default_state()
CONTROL_MODULE = ControlModule(BOARD, STATE)


def start_control_module():
    """Run the control module main loop."""
    CONTROL_MODULE.start()


def update_control_module_state():
    """Change the control module state."""
    sleep(1)
    state = modify_state(STATE, animated=True)
    CONTROL_MODULE.update_config(state)
    # TODO TEST CODE HERE
    while True:
        sleep(1)


def main():
    """Copilot entrance point."""

    control_module_thread = Thread(target=start_control_module, daemon=True)
    control_module_thread.start()

    state_update_thread = Thread(target=update_control_module_state,
                                 daemon=True)
    state_update_thread.start()

    EMULATOR.display()


if __name__ == '__main__':
    main()
