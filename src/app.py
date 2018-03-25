# -*- coding: utf-8 -*-

import sys

import os
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication

from pluto.video.ui.mvc.controllers import MainController, ImageStitchingController
from pluto.video.ui.mvc.routers import Router
from pluto.video.ui.mvc.views import VideoWindow
from pluto.video.ui.player.controller import PlayerController
from pluto.video.ui.qtutils import QtUtil

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(QtUtil.resource_path(os.path.join('windows', 'pluto.png'))))
    router = Router(app)
    main = MainController(router)
    view = VideoWindow(main)
    view.resize(800, 600)
    router.add_ctrl('main', main)
    router.add_ctrl('player', PlayerController(router))
    router.add_ctrl('image', ImageStitchingController(router))
    router.go('player')
    sys.exit(app.exec_())
