"""Control module."""

import asyncio

from pico_copilot.modules.led import LedManager
from pico_copilot.modules.sensor import SensorManager
from pico_copilot.modules.power import PowerModule
from pico_copilot.modules.board_interface import BoardInterface
from pico_copilot.modules.button import ButtonModule
from pico_copilot.modules.state import State
from pico_copilot.utils.logger import LOG


class ControlModule:
    """Module to control launch of all other modules."""

    def __init__(self, board, state):
        """All modules initialization."""
        self._tick = 0.01
        self._board = board
        self._state = State(state)
        self._brightness_map_index = 0
        self._brightness_map = [
            # bri auto_brightness
            (0.5,
             True),
            (0.5,
             False),
            (1.0,
             False)
        ]
        self._ninja_mode = False
        self._ninja_mode_enabled = False

        self._event_mapping = {
            'toggle_brightness': self._toggle_brightness,
            'change_animation': self._change_animation,
            'ninja_mode': self._toggle_ninja_mode,
        }

        self._modules = {}
        self._create_led_module('tail')
        self._create_led_module('front')
        self._create_led_module('status')
        self._create_sensors_module('light')
        self._create_buttons_module('button1')

        self._set_animations()

    async def start(self):
        """Start the control module routine."""
        LOG.info('Control module started')

        tasks = [None] * len(self._modules.values())
        while True:
            self._update_ninja_mode()
            self._update_auto_brightness_modifier()

            # Defer module updates
            for index, module in enumerate(self._modules.values()):
                tasks[index] = asyncio.create_task(module.update())

            await asyncio.sleep(self._tick)

            self._handle_button_events()

            await asyncio.gather(*tasks)

    def _create_led_module(self, name):
        self._modules[f'{name}_leds'] = LedManager(self._board,
                                                   self._state,
                                                   name,
                                                   self._tick)

    def _create_sensors_module(self, name):
        self._modules['sensors'] = SensorManager(self._board,
                                                 self._state,
                                                 name,
                                                 self._tick)

    def _create_buttons_module(self, name):
        self._modules['button'] = ButtonModule(self._board,
                                               self._state,
                                               name,
                                               self._tick)

    def _set_animations(self):
        """Set initial animations."""
        for group in ('tail', 'front', 'status'):
            if self._state.get_leds_state(group)['animation_playing']:
                animation = self._state.get_leds_state(
                    group)['animation_playing']
                mode = self._state.get_leds_state(group)['animation_mode']

                LOG.info(f'Playing "{animation}" on {group}_leds ({mode})')
                self._modules[f'{group}_leds'].set_animation(animation, mode)

    def _update_ninja_mode(self):
        if self._ninja_mode:
            if not self._ninja_mode_enabled:
                self._ninja_mode_to_modules(True)
                self._ninja_mode_enabled = True
        else:
            if self._ninja_mode_enabled:
                self._ninja_mode_to_modules(False)
                self._ninja_mode_enabled = False

    def _update_auto_brightness_modifier(self):
        brightness, auto = self._brightness_map[self._brightness_map_index]
        if auto:
            brightness = self._state.get_sensor('light')

        for module in ['tail_leds', 'front_leds']:
            self._modules[module].set_auto_brightness_modifier(brightness)

        # Hardcode status LED brightness modifier
        # status_led_brightness_modifier = max(brightness, 0.5)
        # self._modules['status_leds'].set_auto_brightness_modifier(
        #     status_led_brightness_modifier)

    def update_config(self, state):
        """Externally change the state."""
        LOG.info('State was overwritten.')
        self._state.update(state)
        self._set_animations()

    def _handle_button_events(self):
        for event, happened in self._state.get_button('button1').items():
            if happened:
                LOG.debug(f'Event {event} happened')
                self._state.remove_button_event('button1', event)
                action = self._state.get_events()[event]
                if action:
                    self._event_mapping[action]()
                else:
                    LOG.info(f'No action was set for {event}')

    def _toggle_brightness(self):
        LOG.debug('Toggle brightness')
        self._brightness_map_index += 1
        if self._brightness_map_index >= len(self._brightness_map):
            self._brightness_map_index = 0

    def _change_animation(self):
        LOG.debug('Change animation')
        # TBD

    def _toggle_ninja_mode(self):
        LOG.debug('Toggle ninja mode')
        self._ninja_mode = not self._ninja_mode

    def _ninja_mode_to_modules(self, state):
        LOG.debug(f'Ninja mode: {state}')
        for module in self._modules.values():
            module.set_ninja_mode(state)
