import os
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QLabel

from pluto.utils import TimeUtil
from pluto.video.ui.mvc.views import View
from pluto.video.ui.qtutils import QtUtil


class PlayerWindow(View):
    def __init__(self):
        super(PlayerWindow, self).__init__()
        uic.loadUi(QtUtil.resource_path(os.path.join("windows", "video_player_window.ui")), self)
        self.setWindowTitle("Pluto Video Snapshotor")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget(self.videoBackgroundWidget)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoBackgroundWidget.setStyleSheet("QWidget { background-color : black;}")
        self.progressLabel = QLabel("00:00:00")
        self.statusbar.addWidget(self.progressLabel)
        self.messageLabel = QLabel("")
        self.statusbar.addWidget(self.messageLabel)
