"""Config."""


BOARD_CONFIG = {
    'leds':
    {
        'tail': {
            'leds': {
                'tail_bars': {'pin': 2},
                'top_v': {'pin': 2},
                'mid_v': {'pin': 2},
                'low_x': {'pin': 2},
            }
        },
        'front': {
            'leds': {
                'front_bars': {'pin': 2},
                'segment_edge': {'pin': 2},
                'segment_mid': {'pin': 2},
                'segment_center': {'pin': 2},
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
}
