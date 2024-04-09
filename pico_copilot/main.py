"""Main entrance point."""


from modules.control import ControlModule
from utils.logger import LOG


def main():
    """Copilot entrance point."""
    LOG.info('Starting the copilot')

    control_module = ControlModule()
    control_module.start()


if __name__ == '__main__':
    main()
