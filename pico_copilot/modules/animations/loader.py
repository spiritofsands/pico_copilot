"""
Animation loader.

Format:
JSON with individual LED instructions.
"""

from json import loads

import pico_copilot
from pico_copilot.utils.logger import LOG


class Loader:

    def __init__(self, animation_name, tick_length):
        self.animation = None
        self.animation_name = animation_name

        self._transition_scale = 10
        self.length = 0
        self._tick = tick_length

        self._load_animation()

    def _load_animation(self):
        copilot_dir = pico_copilot.__file__
        copilot_dir = '/'.join(list(copilot_dir.split('/')[0:-1]))
        resource = '/'.join([copilot_dir, 'resources', 'led_animations.json'])
        animations = loads(open(resource).read())
        animation = animations[self.animation_name]
        extend = animation["config"]["extend"]
        self.animation = animation["data"]

        if extend:
            self._extend_animation()

        self._calculate_animation_length()

    def _extend_animation(self):
        tick = self._tick * self._transition_scale

        extended_animation = []
        for row in self.animation:
            row_length = len(row)
            extended_row = []
            for index in range(row_length - 1):
                # print(f'{row[index]} and {row[index+1]}')

                transition = row[index + 1][0]
                ticks = int(transition // tick)
                last_tick_length = transition % tick
                extended_list = []
                extended_list.append(row[index])
                extended_list.extend(
                    [[tick,
                      value] for value in self._generate_values_between(
                          row[index][1],
                          row[index + 1][1],
                          ticks)])
                if last_tick_length:
                    extended_list.append([last_tick_length, row[index + 1][1]])
                # print(f'extended_list = {extended_list}')
                extended_row.extend(extended_list)
            extended_animation.append(extended_row)

        # from pprint import pprint
        # print('original animation:')
        # pprint(self.animation)
        # print('extended animation:')
        # pprint(extended_animation)
        self.animation = extended_animation

    def _generate_values_between(self, a, b, ticks):
        step = (b - a) / (ticks)
        value = a + step
        # print(f'a = {a}')
        # print(f'b = {b}')
        # print(f'ticks = {ticks}')
        # print(f'step = {step}')
        for _ in range(ticks - 1):
            yield value
            value += step

    def _calculate_animation_length(self):
        list_of_lengths = [len(sublist) for sublist in self.animation]
        self.length = max(list_of_lengths)
