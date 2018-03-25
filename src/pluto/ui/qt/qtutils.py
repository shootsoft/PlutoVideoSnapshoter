# -*- coding: utf-8 -*-

import os

import sys
from PyQt5.QtGui import QPixmap

from pluto.common.utils import SizeUtil


class QtUtil(object):

    @staticmethod
    def preview_image(image_file, label, parent):
        if not os.path.isfile(image_file):
            return False
        image_preview = QPixmap(image_file)
        label.setPixmap(image_preview)
        QtUtil.central(label, parent, image_preview.width(), image_preview.height())

    @staticmethod
    def central(child, parent, width, height, offset_x=0, offset_y=0):
        size = SizeUtil.fit(width - offset_x * 2, height - offset_y * 2, parent.width(), parent.height())
        child.setGeometry((parent.width() - size.width) / 2 + offset_x,
                          (parent.height() - size.height) / 2 + offset_y,
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
