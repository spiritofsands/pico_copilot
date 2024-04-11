"""Custom logger module for raspberry pico."""


class PicoLogger:
    FILENAME = 'log.txt'

    def __init__(self, name):
        self.name = name
        # TBD: control file size
        # TBD: buffering
        with open(self.FILENAME, 'w', encoding='utf-8') as file:
            file.write('------------------------------------\n')

    def debug(self, text):
        print(f'DEBUG: {text}')
        with open(self.FILENAME, 'a', encoding='utf-8') as file:
            file.write(f'DEBUG: {text}\n')

    def info(self, text):
        print(f'INFO: {text}')
        with open(self.FILENAME, 'a', encoding='utf-8') as file:
            file.write(f'DEBUG: {text}\n')



def getLogger(name):
    return PicoLogger(name)

def basicConfig(*args, **kwargs):
    # TBD
    pass
