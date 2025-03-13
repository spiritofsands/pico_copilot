"""Custom logger module for raspberry pico."""

from os.path import getsize


class PicoLogger:
    FILENAME = 'log.txt'

    def __init__(self, name):
        self.name = name

        self._max_file_size = 1024 * 4  # 4 kb
        self._file_size = self._get_file_size()

        # TBD: buffering
        with open(self.FILENAME,
                  self._get_file_mode(),
                  encoding='utf-8') as file:
            self._write(file, '------------------------------------\n')

    def debug(self, text):
        print(f'DEBUG: {text}')
        with open(self.FILENAME,
                  self._get_file_mode(),
                  encoding='utf-8') as file:
            self._write(file, f'DEBUG: {text}\n')

    def info(self, text):
        print(f'INFO: {text}')
        with open(self.FILENAME,
                  self._get_file_mode(),
                  encoding='utf-8') as file:
            self._write(file, f'INFO: {text}\n')

    def warning(self, text):
        print(f'WARNING: {text}')
        with open(self.FILENAME,
                  self._get_file_mode(),
                  encoding='utf-8') as file:
            self._write(file, f'WARNING: {text}\n')

    def _get_file_size(self):
        try:
            return getsize(self.FILENAME)
        except OSError:
            return 0

    def _get_file_mode(self):
        if self._file_size >= self._max_file_size:
            # Check calculations
            current_file_size = self._get_file_size()
            if current_file_size != self._file_size:
                print(f'Current file size {current_file_size} differs from '
                      f'a calculated one {self._file_size}')

            self._file_size = 0
            return 'w'
        return 'a'

    def _write(self, file, text):
        text_size = len(text.encode('utf-8'))
        file.write(text)
        self._file_size += text_size


def getLogger(name):
    return PicoLogger(name)


def basicConfig(*args, **kwargs):
    # TBD
    pass
