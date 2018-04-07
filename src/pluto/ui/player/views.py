# -*- coding: utf-8 -*-
from PyQt5 import Qt

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

from pluto.ui.qt.mvc.views import View


class PlayerWindow(View):
    def __init__(self):
        super(PlayerWindow, self).__init__(ui_file="video_player_window.ui")
        self.videoWidget = QVideoWidget(self.videoBackgroundWidget)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoBackgroundWidget.setStyleSheet("QWidget { background-color : black;}")
        self.progressLabel = QLabel("00:00:00")
        self.statusbar.addWidget(self.progressLabel)
        self.messageLabel = QLabel("")
        self.statusbar.addWidget(self.messageLabel)


