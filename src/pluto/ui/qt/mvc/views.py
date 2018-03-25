# -*- coding: utf-8 -*-
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from pluto.ui.qt.qtutils import QtUtil


class View(QMainWindow):
    def __init__(self, parent=None, ui_path="windows", ui_file=""):
        super(View, self).__init__(parent)
        if ui_file:
            uic.loadUi(QtUtil.resource_path(os.path.join(ui_path, ui_file)), self)
