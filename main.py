"""Main entrance point."""


from pico_copilot.modules.control import ControlModule
from pico_copilot.modules.board_interface import BoardInterface
from pico_copilot.board.board import Board
from pico_copilot.utils.logger import LOG


def main():
    """Copilot entrance point."""
    LOG.info('Starting the copilot')

    board_config = None
    board = Board(board_config)
    board_interface = BoardInterface(board, board_config)

    state = None
    control_module = ControlModule(board_interface, state)
    control_module.start()


if __name__ == '__main__':
    main()
