import cv2
import importlib
from time import sleep
from termcolor import colored


class VideoLoop(object):

    def __init__(self, video):
        # capturing video
        self.paused = False
        self.show_filter = False
        self.filter = None
        self.config = {}
        self.filter_class = None
        self.set_src(video)

    def __del__(self):
        # releasing camera
        self.capture.release()

    def set_src(self, video):
        self.time = 0  # realistcally this is the frame but frame is often used soo

        self.video_src = video
        self.capture = cv2.VideoCapture(video)
        self.last_frame = None
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        print(f"FPS {self.fps}")
        self.cached_video = CachedVideo()
        self.last_log = ''

    def send_error(self, error_msg):
        pass

    def load_mask_module(self):
        if self.filter_class is not None:
            try:
                module = __import__(
                    self.filter_class.__module__, fromlist=[''])
                importlib.reload(module)
                self.filter_class = getattr(module, self.filter_class.__name__)
                del self.filter
                self.filter = self.filter_class(self.config)
                self.config = self.filter.config
                self.cached_video = CachedVideo()
                self.get_frame(skip=False)
                #  print('Selected Load')
            except ModuleNotFoundError:
                print('Invalid module')
                self.send_error("Module not found.")
                self.filter = None
        else:
            print('MASK MODULE NOT SELECTED')
            self.filter = None
            self.cached_video = CachedVideo()

    def add_filter(self, frame):
        if self.filter is None:
            self.load_mask_module()
        if self.filter is None:
            return False
        masked_frame = self.filter.build(
            frame=frame, time=self.capture.get(cv2.CAP_PROP_POS_MSEC))
        return masked_frame

    def change_config(self, key, value):
        self.filter.modify_key(key, value)
        self.config = self.filter.config
        self.cached_video = CachedVideo()
        self.load_mask_module()

    def toggle_pause(self):
        self.paused = not self.paused

    def show_filter_change(self, value):
        if self.show_filter != value:
            self.load_mask_module()
            self.show_filter = value

    def get_frame(self, skip=True):
        frame = self.build_frame(skip)
        try:
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                print(colored("FAIL HERE", "red"))
            sleep(1/self.fps)
            return jpeg.tobytes()
        except TypeError:
            print(f"TYPE ERROR HERE {self.last_log}")
            return self.get_frame()

    def build_frame(self, skip=True):
        if skip and self.paused and self.last_frame is not None:
            self.last_log = 'PAUSED'
            return self.last_frame

        if self.cached_video.ready is True:
            if not self.show_filter:
                del self.cached_video
                self.cached_video = CachedVideo()
                return self.get_frame()
            frame = self.cached_video.next_frame()
            self.last_frame = frame
            self.last_log = 'CACHED'
            return frame

        else:
            if not skip:
                ret, frame = True, self.last_frame
            else:
                ret, frame = self.capture.read()
            if not ret:
                self.capture = cv2.VideoCapture(self.video_src)
                self.last_log = 'ReLAy'
                return self.get_frame(skip)

            if self.show_filter:
                frame = self.add_filter(frame)
                if frame is False:
                    print('ERROR')
                    return
                num = self.capture.get(0)
                self.cached_video.add_frame(frame, num)
            else:
                del self.cached_video
                self.cached_video = CachedVideo()
            self.last_frame = frame
            self.last_log = 'NORMAL'
            return frame


class CachedVideo(object):

    def __init__(self):
        self.frames = []
        self.current_frame = 0
        self.ready = False
        self.start = None

    def __del__(self):
        self.frames = []
        self.ready = False

    def add_frame(self, frame, frame_num):
        if len(self.frames) == 0:
            self.start = frame_num
        elif frame_num == self.start:
            self.play()
            return
        self.frames.append(frame)
        self.current_frame += 1

    def next_frame(self):
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        return self.frames[self.current_frame]

    def play(self):
        # print('Start cache video')
        # print(self.start)
        self.ready = True
        self.current_frame = 0
