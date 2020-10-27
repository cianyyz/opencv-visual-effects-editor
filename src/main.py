from flask import Flask, render_template, Response, request
from picture import VideoLoop
import importlib
import os
import json
from cv2 import imread, imencode
from os import listdir
from os.path import isfile, join

from modules import *
from modules.base_module import BaseModule

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')


@app.route('/module_config_panel/', methods=['GET', 'POST'])
def module_config_panel(config={}):
    if vid is not None and vid.filter is not None:
        config = vid.filter.config
    else:
        if vid is not None:
            vid.filter_class = vid.filter_class if vid.filter_class is not None else classes[
                0]
            vid.filter = vid.filter_class(config)
        else:
            config = classes[0](config).config

    return render_template('module_config_panel.html', config=config)


@app.route('/module_config_panel/submit', methods=['GET', 'POST'])
def module_config_panel_submit():
    form = request.form
    val = form['val']
    val = True if val == 'true' else val
    val = False if val == 'false' else val
    vid.change_config(key=form['key'], value=val)
    vid.filter = None
    vid.load_mask_module()
    return "", 200


@app.route('/module_settings')
def module_settings():
    filtered = 'checked' if vid is not None and vid.show_filter is True else ''
    paused = 'paused' if vid is not None and vid.paused is True else ''
    curr_class = vid.filter_class.__name__ if vid is not None and vid.filter_class is not None else None
    return render_template('module_settings.html', current_class=curr_class, classes=vclass, filtered=filtered, paused=paused, videos=videos)


@app.route('/module_settings_form')
def module_settings_form():
    if vid.filter_class.__name__ != classes[vclass.index(request.args['class'])].__name__:
        vid.filter_class = classes[vclass.index(request.args['class'])]
        vid.config = {}
        vid.load_mask_module()
    vid.show_filter_change(
        value=True if request.args['show'] == 'true' else False)
    vid.paused = True if request.args['paused'] == 'true' else False
    return "", 200


def gen(VideoLoop):
    while True:
        if vid is None:
            frame = imread(os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'static', 'img', 'video_not_found.png'))
            ret, png = imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + png.tobytes() + b'\r\n\r\n')
        else:
            frame = VideoLoop.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(vid),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/change_video_src', methods=['GET', 'POST'])
def change_video_src():
    print(request.args)
    print(request.form)
    print(request.values)
    vid.set_src(video=os.path.join(videos_path, request.args.get('video')))
    # vid.set_src(file)
    return '', 200


def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))
    return all_subclasses


def get_settings():
    with open(config_file) as json_data_file:
        data = json.load(json_data_file)
        return data


def save_settings():
    with open(config_file, 'w') as outfile:
        json.dump(settings, outfile)


if __name__ == '__main__':
    # defining server ip address and port
    classes = get_all_subclasses(BaseModule)
    vclass = [x.__name__ for x in classes]
    config_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'config.json')
    settings = get_settings()

    vid = VideoLoop(video=settings['video_src']
                    if 'video_src' in settings and settings['video_src'] is not None else os.path.join(os.path.dirname(
                        os.path.abspath(__file__)), 'static', 'video', 'big_buck_bunny.mp4'))

    videos_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'static', 'video')
    videos = [f for f in listdir(videos_path) if isfile(join(videos_path, f))]
    print(videos)
    app.run(debug=True)
