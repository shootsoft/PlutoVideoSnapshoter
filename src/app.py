# -*- coding: utf-8 -*-

import sys

import os
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication

from pluto.ui.player.controllers import PlayerController
from pluto.ui.qt.mvc.routers import Router
from pluto.ui.stitcher.controllers import ImageStitchingController
from pluto.ui.qt.qtutils import QtUtil
import qdarkstyle

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setWindowIcon(QtGui.QIcon(QtUtil.resource_path(os.path.join('windows', 'pluto.png'))))
    router = Router(app)
    router.add_ctrl('player', PlayerController(router))
    router.add_ctrl('image', ImageStitchingController(router))
    router.go('player')
    sys.exit(app.exec_())
