"""Logger config module."""

import asyncio
from time import sleep
from sys import print_exception

from pico_copilot.utils.logger import LOG


def failsafe_loop(starting_function):
    """Copilot entrance point."""
    while True:
        try:
            LOG.info('Clear starting the copilot')
            asyncio.run(starting_function())
        except KeyboardInterrupt:
            LOG.error('Keyboard interrupt')
            raise
        except BaseException as e:
            LOG.error(f'Caught exception: {repr(e)}!')
            LOG.error(print_exception(e))

        LOG.info('Restarting...')
        sleep(1)
