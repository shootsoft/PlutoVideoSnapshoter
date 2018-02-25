"""
Usage:
    python build.py
"""
import os

import sys
from setuptools import setup

sys.argv.append('py2app')
APP = ['src/app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'res/pluto.icns',
    'plist': {'CFBundleShortVersionString': '1.1', },
    'includes': ['sip', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'opencv-python', 'numpy', 'Pillow'],
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
