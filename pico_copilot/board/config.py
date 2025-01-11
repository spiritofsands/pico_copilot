"""Config."""

BOARD_CONFIG = {
    'leds': {
        'tail': {
            'leds': {
                'tail_bars': {
                    'pin': 14
                },
                'top_v': {
                    'pin': 15
                },
                'mid_v': {
                    'pin': 16
                },
                'low_x': {
                    'pin': 17
                },
            }
        },
        'front': {
            'leds': {
                'front_bars': {
                    'pin': 18
                },
                'segment_edge': {
                    'pin': 19
                },
                'segment_mid': {
                    'pin': 20
                },
                'segment_center': {
                    'pin': 21
                },
            }
        },
        'status': {
            'leds': {
                'status': {
                    'pin': 22
                },
            }
        }
    },
    'sensors': {
        'light': {
            'sda': 26,
            'scl': 27,
            'i2c': 1,
            'device_address': 0x23,
        },
    },
    'buttons': {
        'button1': {
            'pin': 28,
        },
    },
}
