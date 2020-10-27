default_types = {
    'integer': {
        'type': int,
        'visual_type': 'increment_checkbox',
        'default': 0,
        'min': -100,
        'max': 100
    },
    'float': {
        'type': float,
        'visual_type': 'slider',
        'default': 0,
        'min': -1.0,
        'max': 1.0
    },
    'boolean': {
        'type': bool,
        'visual_type': 'checkbox',
        'default': False,
        'min': None,
        'max': None
    },
    'string': {
        'type': str,
        'visual_type': 'text_input',
        'default': '',
        'min': None,
        'max': None
    },
    'color': {
        'type': Color,
        'visual_type': 'color_picker',
        'default': '#ffffff',
        'arr': [255, 255, 255],
        'min': None,
        'max': None
    },
    'module': {
        'type': str,
        'visual_type': 'text_input',
        'default': '',
        'min': None,
        'max': None
    }
}


class BaseConfigType:
    def __init__(self, settings):
        self.settings = {}
