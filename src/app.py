import sys
from PyQt5.QtWidgets import QApplication

from pluto.video.ui.mvc.controllers import MainController
from pluto.video.ui.mvc.views import VideoWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ctrl = MainController(app)
    view = VideoWindow(ctrl)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())