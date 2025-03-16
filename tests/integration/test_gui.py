"""Main entrance point."""

import asyncio
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
from pico_copilot.utils.failsafe_loop import failsafe_loop

BOARD_CONFIG = {
    'leds': {
        'tail': {
            'leds': {
                'tail_1': {
                    'pin': 1
                },
                'tail_2': {
                    'pin': 2
                },
                'tail_3': {
                    'pin': 3
                },
                'tail_4': {
                    'pin': 4
                },
            }
        },
        'front': {
            'leds': {
                'front_1': {
                    'pin': 5
                },
                'front_2': {
                    'pin': 6
                },
                'front_3': {
                    'pin': 7
                },
                'front_4': {
                    'pin': 8
                },
            }
        },
        'status': {
            'leds': {
                'status': {
                    'pin': 9
                },
            }
        }
    },
    'sensors': {
        'light': {
            'pin': 10
        },
    },
}


def generate_default_state():
    # Virtual initial state
    return {
        'leds':
        {
            'tail': {
                'state': {
                    'hardware_brightness_modifier': 1.0,
                    'animation_playing': None,
                    'animation_mode': 'once',
                    'animation_finished': False,
                },
                'leds': {
                    'tail_1': {'brightness': 0},
                    'tail_2': {'brightness': 0},
                    'tail_3': {'brightness': 0},
                    'tail_4': {'brightness': 0},
                }
            },
            'front': {
                'state': {
                    'hardware_brightness_modifier': 0.8,
                    'animation_playing': None,
                    'animation_mode': 'once',
                    'animation_finished': False,
                },
                'leds': {
                    'front_1': {'brightness': 0},
                    'front_2': {'brightness': 0},
                    'front_3': {'brightness': 0},
                    'front_4': {'brightness': 0},
                }
            },
            'status': {
                'state': {
                    'hardware_brightness_modifier': 0.7,
                    'animation_playing': None,
                    'animation_mode': 'once',
                    'animation_finished': False,
                },
                'leds': {
                    'status': {'brightness': 0},
                }
            }
        },
        'sensors':
        {
            'light':
            {
                'value': 0,
                'update_interval': 1,  # 1 sec
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
    }


# TODO: use in tests or remove
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


async def control_module_clear_start():
    state = generate_default_state()
    control_module = ControlModule(BOARD, state)
    await control_module.start()


def control_module():
    failsafe_loop(control_module_clear_start)


def update_control_module_state():
    """Change the control module state."""
    sleep(1)

    # TODO TEST CODE HERE
    while True:
        sleep(1)


def main():
    """Copilot entrance point."""

    control_module_thread = Thread(target=control_module, daemon=True)
    control_module_thread.start()

    state_update_thread = Thread(target=update_control_module_state,
                                 daemon=True)
    state_update_thread.start()

    EMULATOR.display()


if __name__ == '__main__':
    main()
