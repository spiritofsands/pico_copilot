"""Config."""

BOARD_CONFIG = {
    'leds': {
        'tail': {
            'leds': {
                'tail_1': {
                    'pin': 18
                },
                'tail_2': {
                    'pin': 19
                },
                'tail_3': {
                    'pin': 20
                },
                'tail_4': {
                    'pin': 21
                },
            }
        },
        'front': {
            'leds': {
                'front_1': {
                    'pin': 14
                },
                'front_2': {
                    'pin': 15
                },
                'front_3': {
                    'pin': 16
                },
                'front_4': {
                    'pin': 17
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
