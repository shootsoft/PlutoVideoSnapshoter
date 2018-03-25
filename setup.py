# -*- coding: utf-8 -*-
import os

import sys
from setuptools import setup

APP = ['src/app.py']
DATA_FILES = [
    ('windows', ['src/windows/image_stitching_window.ui',
                 'src/windows/video_player_window.ui',
                 'src/windows/pluto.png'
                 ]),
    ('', ['res/qt.conf'])
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'res/pluto.icns',
    'plist': {'CFBundleShortVersionString': '1.4', },
    'includes': ['sip',
                 'opencv-python',
                 'numpy',
                 'Pillow',
                 'PyQt5',
                 'PyQt5.QtCore',
                 'PyQt5.QtGui',
                 'PyQt5.QtWidgets',
                 'PyQt5.QtMultimedia',
                 'PyQt5.QtMultimediaWidgets',
                 'PyQt5.pyqtconfig',
                 'PyQt5._qt',
                 'pluto.*',
                 'pluto.common.media.*',
                 'pluto.ui.*',
                 'pluto.ui.qt.*',
                 'pluto.ui.qt.mvc.*',
                 'pluto.ui.player.*',
                 'pluto.ui.stitcher.*'
                 ],
    'bdist_base': os.path.join(os.getcwd(), 'build', 'build'),
    'dist_dir': os.path.join(os.getcwd(), 'build', 'dist'),
}

setup(
    app=APP,
    name='PlutoVideoSnapshoter',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
