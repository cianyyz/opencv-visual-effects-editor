class Color:
    def __init__(self, value):
        if not Color.is_type_color(value):
            print(f"WRONG COLOR VALUE {value}, please use a 3x1 array")
            raise TypeError
        self.value = value
        self.arr = [int(value[1:3], 16), int(
            value[3:5], 16), int(value[5:], 16)][::-1]

    @staticmethod
    def is_type_color(col):
        '''if type(col) is list and len(col) == 3 :
            bols = [0 <= x <= 255 for x in col]
            return bols[0] and bols[1] and bols[2]'''
        return type(col) is str and len(col) == 7

    @staticmethod
    def decarrtorgbstring(col):
        def hex(x): return hex(x)[2:]
        return f"#{hex(col[0])}{hex(col[1])}{hex(col[2])}"

    @staticmethod
    def decarrtohex(col):
        return f"rgb({col[0]}, {col[1]}, {col[2]})"


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


class BaseModule:

    def __init__(self, config={}):
        self.config = config

    def add_config(self, key, data_type, visual_type=None, default=None, min=None, max=None):
        if data_type not in default_types:
            print(f'WRONG TYPE {data_type}')
            raise TypeError
        settings = default_types[data_type].copy()
        settings['data_type'] = data_type
        print(settings['type'])
        if default is not None:
            if settings['type'] == Color:
                if not Color.is_type_color(default):
                    print('COLOR TYPE ERROR WARNING: Wrong type for default value')
                    raise TypeError
                settings['arr'] = Color(default).arr
            else:
                if type(default) != settings['type']:
                    print('TYPE ERROR WARNING: Wrong type for default value')
                    raise TypeError
            settings['default'] = default
        if visual_type is not None:
            settings['visual_type'] = visual_type
        if min is not None:
            settings['min'] = min
        if max is not None:
            settings['max'] = max
        settings['value'] = settings['default']
        self.config[key] = settings

    def modify_key(self, key, value):
        print(f'CONFIG EDIT {key} is now {value}')
        dclass = self.config[key]['type']
        v = dclass(value)
        if dclass == Color:
            self.config[key]['arr'] = v.arr
            v = v.value
        print(f'{type(v)} == {v}')
        self.config[key]['value'] = v

    def set_config(self, config_dict):
        self.config = config_dict

    def build(self, frame, time):
        pass
