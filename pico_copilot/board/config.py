"""Config."""


BOARD_CONFIG = {
    'leds':
    {
        'tail': {
            'leds': {
                'tail_bars': {'pin': 1},
                'top_v': {'pin': 3},
                'mid_v': {'pin': 4},
                'low_x': {'pin': 5},
            }
        },
        'front': {
            'leds': {
                'front_bars': {'pin': 6},
                'segment_edge': {'pin': 7},
                'segment_mid': {'pin': 8},
                'segment_center': {'pin': 9},
            }
        },
        'status': {
            'leds': {
                'status': {
                    'pin': 18},
            }
        }
    },
    'sensors':
    {
        'light': {
            'sda': 26,
            'scl': 27,
            'i2c': 1,
            'device_address': 0x23,
        },
    },
    'buttons':
    {
        'button1':
        {
            'pin': 22,
        },
    },
}
