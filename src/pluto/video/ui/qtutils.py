import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

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
        if size.width > size.height:
            label.setGeometry(0, (parent.height() - size.height) / 2, size.width, size.height)
        else:
            label.setGeometry((parent.width() - size.width) / 2, 0, size.width, size.height)

