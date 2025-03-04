"""Control module."""

import asyncio

from pico_copilot.modules.led import LedManager
from pico_copilot.modules.sensor import SensorManager
from pico_copilot.modules.power import PowerModule
from pico_copilot.modules.board_interface import BoardInterface
from pico_copilot.modules.button import ButtonModule
from pico_copilot.modules.modes import (
    StartupMode,
    PoweroffMode,
    StaticMode,
    NormalMode,
)
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
        self._mode = None

        # is called by a mapping in the current mode
        self._event_mapping = {
            'poweroff': self._set_poweroff_mode,
            'startup': self._set_startup_mode,
            'static': self._set_static_mode,
            'normal': self._set_normal_mode,
        }

        self._modules = {}
        self._modules['tail_leds'] = LedManager(self._board,
                                                self._state,
                                                'tail',
                                                self._tick)
        self._modules['front_leds'] = LedManager(self._board,
                                                 self._state,
                                                 'front',
                                                 self._tick)
        self._modules['status_leds'] = LedManager(self._board,
                                                  self._state,
                                                  'status',
                                                  self._tick)
        self._modules['sensors'] = SensorManager(self._board,
                                                 self._state,
                                                 'light',
                                                 self._tick)
        self._modules['button1'] = ButtonModule(self._board,
                                                self._state,
                                                'button1',
                                                self._tick)

        # Set the initial mode
        self._update_mode(StartupMode(self._state))

    async def start(self):
        """Start the control module routine."""
        LOG.info('Control module started')

        tasks = [None] * len(self._modules.values())
        while True:
            self._update_auto_brightness_modifier()

            # Defer module updates
            for index, module in enumerate(self._modules.values()):
                tasks[index] = asyncio.create_task(module.update())

            await asyncio.sleep(self._tick)

            self._handle_button_events()
            self._update_mode()

            # TODO: needed?
            await asyncio.gather(*tasks)

    def _toggle_modules(self):
        for module, enabled in self._mode.module_enabled.items():
            self._modules[module].toggle(enabled)

    def _update_mode(self, mode=None):
        """Set a new mode explicitly of implicitly."""
        if not mode:
            mode = self._mode.check_events()

        if mode:
            self._mode = mode
            self._set_animations()
            self._set_brightness()
            self._toggle_modules()

    def _set_animations(self):
        """Set initial animations."""
        for group in ('tail', 'front', 'status'):
            animation = self._state.get_leds_animation_playing(group)
            mode = self._state.get_leds_animation_mode(group)
            self._modules[f'{group}_leds'].set_animation(animation, mode)

    def _set_brightness(self):
        """Set Led brightness."""
        for group in ('tail', 'front', 'status'):
            brightness = self._mode.leds[group]['brightness']
            if brightness:
                self._modules[f'{group}_leds'].set_all_leds_brightness(
                    brightness)

    def _update_auto_brightness_modifier(self):
        brightness = self._state.get_sensor('light')
        for module in ['tail_leds', 'front_leds', 'status_leds']:
            self._modules[module].set_auto_brightness_modifier(brightness)

    # TODO: use for tests or remove
    def update_config(self, state):
        """Externally change the state."""
        LOG.info('State was overwritten.')
        self._state.update(state)
        self._set_animations()
        self._set_brightness()

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

    def _set_static_mode(self):
        self._update_mode(StaticMode(self._state))

    def _set_normal_mode(self):
        self._update_mode(NormalMode(self._state))
