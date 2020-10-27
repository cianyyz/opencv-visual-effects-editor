Visual Effects Editor
==========================

Visual Effects Editor that can preview and tweak paramters in the browser. Hot reloads python modules, for a seamless experience when editing
visual effects utilizing cv2. Built using flask, opencv2, dlib, jinja2, html, css

Features
------------
- Hot Python Module Reloading
- Custom configuration types
- Video caching so only one render per frame is needed
- Time-based filters which allows the creation of transitions

Todo
-------------
- Exporting
- Video playback controls
- Error handling
- Add submodule configuration type
- Make README.md better
- More documentation
- Better UI


Known bugs
-------------
- Cached Video - sometimes will save a frame that should not be in the render
- UI falls apart if video-object crashes
