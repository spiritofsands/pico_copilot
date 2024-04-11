"""
Animations to be used by LEDs.

Format:
List of individual led instructions,
each instruction is a tuple of (seconds, brightness).
"""

from json import loads

import pico_copilot
from pico_copilot.utils.logger import LOG


class Animation:
    def __init__(self, animation_name, tick_length):
        self.finished = False
        self._animation_name = animation_name
        self._animation = None
        self._length = 0
        self._led_count = 0
        self._tick = tick_length

        self._load_animation()
        self._led_count = len(self._animation)
        self._calculate_animation_length()
        self.reset()

    def _load_animation(self):
        copilot_dir = pico_copilot.__file__
        copilot_dir = '/'.join(list(copilot_dir.split('/')[0:-1]))
        resource = '/'.join([copilot_dir, 'resources',
                            'led_animations.json'])
        animations = loads(open(resource).read())
        self._animation = animations[self._animation_name]

    def _calculate_animation_length(self):
        list_of_lengths = [len(sublist) for sublist in self._animation]
        self._length = max(list_of_lengths)

    def _advance_time(self):
        self._time += self._tick

    def reset(self):
        self._load_animation()
        self._indexes = [0] * self._led_count
        self._frame = [led[0] for led in self._animation]
        self._time = 0
        self._index_finished = [False] * self._led_count
        self._led_time = [0.0] * self._led_count
        self.finished = False

    def _check_finished(self):
        self.finished = all(self._index_finished)

    def generate_frame(self):
        """
        Generate a consequent led brightness frame.
        Should be called every tick.
        """
        for led in range(self._led_count):
            if self._indexes[led] >= len(self._animation[led]):  # outof bounds
                self._index_finished[led] = True
                self._check_finished()
            else:
                led_time, led_brightness = self._animation[led][
                    self._indexes[led]]
                self._frame[led] = led_brightness

                # increment led time per frame
                self._led_time[led] += led_time
                # avoid adding the time second time
                self._animation[led][self._indexes[led]] = (
                    0.0, led_brightness)

                if self._time >= self._led_time[led]:
                    next_index = self._indexes[led] + 1
                    if next_index < self._length:
                        self._indexes[led] = next_index
                    else:
                        self._index_finished[led] = True
                        self._check_finished()

        self._advance_time()
        return self._frame
