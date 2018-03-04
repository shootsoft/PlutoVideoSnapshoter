# -*- coding: utf-8 -*-

import os

import sys
from PyQt5.QtGui import QPixmap

from pluto.utils import SizeUtil


class QtUtil(object):

    @staticmethod
    def preview_image(image_file, label, parent):
        if not os.path.isfile(image_file):
            return False
        image_preview = QPixmap(image_file)
        label.setPixmap(image_preview)
        QtUtil.central(label, parent, image_preview.width(), image_preview.height())

    @staticmethod
    def central(label, parent, width, height):
        size = SizeUtil.fit(width, height, parent.width(), parent.height())
        # print width, height, parent.width(), parent.height(), size
        label.resize(size.width, size.height)
        label.setGeometry((parent.width() - size.width) / 2, (parent.height() - size.height) / 2,
                          size.width, size.height)

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
