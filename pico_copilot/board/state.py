"""State."""

_DEFAULT_BRIGHTNESS = 0.5

STATE = {
    'leds':
    {
        'tail': {
            'state': {
                'animation_playing': 'startup',
                'animation_mode': 'repeat',
            },
            'leds': {
                'tail_1': {'brightness': _DEFAULT_BRIGHTNESS},
                'tail_2': {'brightness': _DEFAULT_BRIGHTNESS},
                'tail_3': {'brightness': _DEFAULT_BRIGHTNESS},
                'tail_4': {'brightness': _DEFAULT_BRIGHTNESS},
            }
        },
        'front': {
            'state': {
                'animation_playing': 'startup',
                'animation_mode': 'repeat',
            },
            'leds': {
                'front_1': {'brightness': _DEFAULT_BRIGHTNESS},
                'front_2': {'brightness': _DEFAULT_BRIGHTNESS},
                'front_3': {'brightness': _DEFAULT_BRIGHTNESS},
                'front_4': {'brightness': _DEFAULT_BRIGHTNESS},
            }
        },
        'status': {
            'state': {
                'animation_playing': 'heartbeat',
                'animation_mode': 'repeat',
            },
            'leds': {
                'status': {'brightness': _DEFAULT_BRIGHTNESS},
            }
        }
    },
    'sensors':
    {
        'light':
        {
            'value': _DEFAULT_BRIGHTNESS,
            'update_interval': 1,  # 1 sec
        },
    },
    'buttons':
    {
        'button1':
        {
            'single_click': False,
            'double_click': False,
            'long_click': False,
        },
    },
    'events':  # move to RO config?
    {
        'single_click': '',  # TBD
        'double_click': 'toggle_brightness',
        'long_click': 'ninja_mode',
    }
}
