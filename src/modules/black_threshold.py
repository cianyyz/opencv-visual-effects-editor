import cv2
from .base_module import BaseModule
import numpy as np


class BlackThreshold(BaseModule):

    def __init__(self, config={}):
        super(BlackThreshold, self).__init__(config)
        if config == {}:
            self.add_config(key='color', data_type='color', default='#45e601')
            self.add_config(key='threshold', data_type='integer',
                            visual_type='slider', default=50, min=0, max=255)
            self.add_config(key='invert', data_type='boolean',
                            visual_type='checkbox', default=False)
            self.add_config(key='time_stop', data_type='integer',
                            visual_type='number', default=1250, min=0, max=2000)

    def build(self, frame, time):
        threshold = self.config['threshold']['value']
        color = self.config['color']['arr']
        invert = self.config['invert']['value']
        time_stop = self.config['time_stop']['value']
        input_image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(
            input_image_gray, threshold, 255, cv2.THRESH_BINARY)
        gray_to_black = cv2.cvtColor(blackAndWhiteImage, cv2.COLOR_GRAY2BGR)
        gray_to_black = gray_to_black if not invert else cv2.bitwise_not(
            gray_to_black)
        color_filter = np.full(gray_to_black.shape, color, np.uint8)
        if time_stop != 0:
            color_filter = cv2.addWeighted(color_filter, max(1, time/time_stop),
                                           cv2.bitwise_not(gray_to_black), 1.0, 0)
        black_to_color = cv2.bitwise_and(gray_to_black, color_filter)
        return black_to_color
