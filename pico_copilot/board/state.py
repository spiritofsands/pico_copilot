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
                'tail_bars': {'brightness': _DEFAULT_BRIGHTNESS},
                'top_v': {'brightness': _DEFAULT_BRIGHTNESS},
                'mid_v': {'brightness': _DEFAULT_BRIGHTNESS},
                'low_x': {'brightness': _DEFAULT_BRIGHTNESS},
            }
        },
        'front': {
            'state': {
                'animation_playing': 'startup',
                'animation_mode': 'repeat',
            },
            'leds': {
                'front_bars': {'brightness': _DEFAULT_BRIGHTNESS},
                'segment_edge': {'brightness': _DEFAULT_BRIGHTNESS},
                'segment_mid': {'brightness': _DEFAULT_BRIGHTNESS},
                'segment_center': {'brightness': _DEFAULT_BRIGHTNESS},
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
