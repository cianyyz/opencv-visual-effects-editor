from .base_module import BaseModule
import cv2


class TimeCounter(BaseModule):

    def __init__(self, config={}):
        super(TimeCounter, self).__init__(config)
        if config == {}:
            self.add_config(key='color', data_type='color', default='#ff0000')
            self.add_config(key='stringformat', data_type='boolean',
                            visual_type='checkbox', default=False)
            self.add_config(key='size', data_type='integer',
                            visual_type='slider', default=50, min=0, max=255)

    def build(self, frame, time):
        color = self.config['color']['arr']
        isSeconds = self.config['stringformat']['value']
        size = self.config['size']['value']
        font = cv2.FONT_HERSHEY_SIMPLEX
        string = "{:.2f}".format(
            time/1000)if isSeconds == True else "{:.0f}".format(time)
        print_frame = cv2.putText(
            frame, string, (10, frame.shape[0] - 10), font, 4, color, 2, cv2.LINE_AA)
        return print_frame
