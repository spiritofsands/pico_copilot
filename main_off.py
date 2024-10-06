"""Main entrance point."""

import asyncio

from pico_copilot.modules.control import ControlModule
from pico_copilot.modules.board_interface import BoardInterface
from pico_copilot.board.board import Board
from pico_copilot.board.config import BOARD_CONFIG
from pico_copilot.board.state import STATE
from pico_copilot.utils.logger import LOG


def main():
    """Copilot entrance point."""
    LOG.info('Starting the copilot')

    board_config = BOARD_CONFIG
    board = Board(board_config)
    board_interface = BoardInterface(board, board_config)

    state = STATE
    # LOG.debug(f'INIT STATE: {state}')
    control_module = ControlModule(board_interface, state)
    asyncio.run(control_module.start())


if __name__ == '__main__':
    main()
