"""Control module."""

import asyncio

from pico_copilot.modules.led import LedManager
from pico_copilot.modules.sensor import SensorManager
from pico_copilot.modules.power import PowerModule
from pico_copilot.modules.board_interface import BoardInterface
from pico_copilot.modules.button import ButtonModule
from pico_copilot.modules.modes import StartupMode, PoweroffMode
from pico_copilot.modules.state import State
from pico_copilot.utils.logger import LOG


class ControlModule:
    """Module to control launch of all other modules."""

    def __init__(self, board, state):
        """All modules initialization."""
        # event handling speed
        self._tick = 0.01
        self._board = board
        self._state = State(state)
        self._brightness_map_index = 0
        # changed by a doubleclick
        self._brightness_map = [
            # bri auto_brightness
            (0.5,
             True),
            (0.5,
             False),
            (1.0,
             False)
        ]
        # TODO: remove
        self._ninja_mode = False
        self._ninja_mode_enabled = False

        # is called by a mapping in the current mode
        self._event_mapping = {
            'toggle_brightness': self._toggle_brightness,
            'change_animation': self._change_animation,
            'poweroff': self._set_poweroff_mode,
            'startup': self._set_startup_mode,
        }

        # initial mode
        self._mode = StartupMode(self._state)

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
            # TODO: remove
            self._update_ninja_mode()

            self._update_auto_brightness_modifier()

            # Defer module updates
            for index, module in enumerate(self._modules.values()):
                tasks[index] = asyncio.create_task(module.update())

            await asyncio.sleep(self._tick)

            self._handle_button_events()
            self._update_mode()

            # TODO: needed?
            await asyncio.gather(*tasks)

    def _update_mode(self, mode=None):
        if not mode:
            mode = self._mode.check_events()

        if mode:
            self._mode = mode
            self._set_animations()

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
            animation = self._mode.animation[group]['name']
            mode = self._mode.animation[group]['mode']
            if animation and mode:
                self._state.set_leds_state(group,
                                           'animation_playing',
                                           animation)
                self._state.set_leds_state(group, 'animation_mode', mode)

                LOG.info(f'Playing "{animation}" on {group}_leds ({mode})')
                # TODO: why not from a state?
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
        if auto and self._mode.auto_brightness:
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
        if self._state.has_button_events('button1'):
            for event in self._state.get_button_events('button1'):
                happened = self._state.retrieve_button_event('button1', event)
                if happened:
                    LOG.debug(f'Event {event} happened')
                    action = self._mode.button_actions[event]
                    if action:
                        self._event_mapping[action]()
                    else:
                        LOG.info(f'No action was set for {event}')

    def _set_poweroff_mode(self):
        self._update_mode(PoweroffMode(self._state))

    def _set_startup_mode(self):
        self._update_mode(StartupMode(self._state))

    def _toggle_brightness(self):
        LOG.debug('Toggle brightness')
        self._brightness_map_index += 1
        if self._brightness_map_index >= len(self._brightness_map):
            self._brightness_map_index = 0

    def _change_animation(self):
        LOG.debug('Change animation')
        # TBD

    def _ninja_mode_to_modules(self, state):
        LOG.debug(f'Ninja mode: {state}')
        for module in self._modules.values():
            module.set_ninja_mode(state)
