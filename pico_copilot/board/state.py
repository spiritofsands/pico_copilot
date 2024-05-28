"""State."""

_DEFAULT_BRIGHTNESS = 0.5

STATE = {
    'leds':
    {
        'tail': {
            'state': {
                'animation_playing': None,
                'animation_mode': 'once',
            },
            'leds': {
                'tail_bars': {'brightness': _DEFAULT_BRIGHTNESS},
                'top_v': {'brightness': 0},
                'mid_v': {'brightness': 0},
                'low_x': {'brightness': 0},
            }
        },
        'front': {
            'state': {
                'animation_playing': None,
                'animation_mode': 'once',
            },
            'leds': {
                'front_bars': {'brightness': _DEFAULT_BRIGHTNESS},
                'segment_edge': {'brightness': 0},
                'segment_mid': {'brightness': 0},
                'segment_center': {'brightness': 0},
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
