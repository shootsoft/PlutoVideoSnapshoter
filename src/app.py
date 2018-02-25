# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from pluto.video.ui.mvc.controllers import MainController, ImageStitchingController
from pluto.video.ui.mvc.routers import Router
from pluto.video.ui.mvc.views import VideoWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    router = Router(app)
    main = MainController(router)
    view = VideoWindow(main)
    view.resize(800, 600)
    router.add_ctrl('main', main)
    router.add_ctrl('image', ImageStitchingController(router))
    router.go('main')
    sys.exit(app.exec_())
