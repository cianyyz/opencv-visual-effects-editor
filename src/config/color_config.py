
from base_config_type import BaseConfigType


class ColorConfig(BaseConfigType):

    def __init__(self, settings):
        super(ColorConfig, self).__init__(settings)

    def modify_config(self, key, value):
        if not ColorConfig.is_type(value):
            print(f"WRONG COLOR VALUE {value}, please use '#hex' ")
            raise TypeError
        self.settings[key]['arr'] = [int(value[1:3], 16), int(
            value[3:5], 16), int(value[5:], 16)][::-1]
        self.settings[key]['value'] = value

    @staticmethod
    def is_type(possible_color):
        type(col) is str and len(col) == 7
