"""State."""

_DEFAULT_BRIGHTNESS = 0.5

STATE = {
    'leds':
    {
        'tail': {
            'state': {
                'hardware_brightness_modifier': 1.0,
                'animation_playing': 'startup',
                'animation_mode': 'repeat',
                'animation_finished': False,
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
                'hardware_brightness_modifier': 0.8,
                'animation_playing': 'startup',
                'animation_mode': 'repeat',
                'animation_finished': False,
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
                'hardware_brightness_modifier': 0.7,
                'animation_playing': 'heartbeat',
                'animation_mode': 'repeat',
                'animation_finished': False,
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
    # TODO: remove
    'events':  # move to RO config?
    {
        'single_click': '',  # TBD
        'double_click': 'toggle_brightness',
        'long_click': 'ninja_mode',
    }
}
