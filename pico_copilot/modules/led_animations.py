"""
Animations to be used by LEDs.

Format:
List of individual led instructions,
each instruction is a tuple of (seconds, brightness).
"""

from copy import deepcopy


ANIMATIONS = {
    'startup': [
        # sec  bri
        [(0.5, 1.0)],
        [(0.5, 1.0), (0.0, 0.0)],
        [(0.5, 0.0), (0.5, 1.0), (0.0, 0.0)],
        [(1.0, 0.0), (0.5, 1.0)],
    ],
    'heartbeat': [
        [(0.1, 1.0), (0.9, 0.0)],
    ],
    'slow_heartbeat': [
        [(0.1, 1.0), (2.9, 0.0)],
    ],
}


class Animation:
    def __init__(self, animation_name, tick_length):
        self.finished = False
        self._animation_name = animation_name
        self._animation = deepcopy(ANIMATIONS[animation_name])
        self._length = self._get_animation_length()
        self._led_count = len(self._animation)
        self._tick = tick_length

        self.reset()

    def _get_animation_length(self):
        list_of_lengths = [len(sublist) for sublist in self._animation]
        return max(list_of_lengths)

    def _advance_time(self):
        self._time += self._tick

    def reset(self):
        self._animation = deepcopy(ANIMATIONS[self._animation_name])
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
