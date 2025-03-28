"""Main entrance point."""

import asyncio

from pico_copilot.modules.control import ControlModule
from pico_copilot.modules.board_interface import BoardInterface
from pico_copilot.board.board import Board
from pico_copilot.board.config import BOARD_CONFIG
from pico_copilot.board.state import STATE
from pico_copilot.utils.failsafe_loop import failsafe_loop

BOARD = Board(BOARD_CONFIG)
BOARD_INTERFACE = BoardInterface(BOARD, BOARD_CONFIG)


async def control_module_clear_start():
    """Start the system."""
    state = STATE
    # LOG.debug(f'INIT STATE: {state}')
    control_module = ControlModule(BOARD_INTERFACE, state)
    await control_module.start()


if __name__ == '__main__':
    failsafe_loop(control_module_clear_start)
