# -*- coding: utf-8 -*-
import os
from PyQt5 import Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton

from pluto.ui.qt.mvc.views import View

import icons

from pluto.ui.qt.qtutils import QtUtil


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
        self.mediaPositionSlider.setStyleSheet("""
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
            border: 0px solid #5c5c5c;
            width: 16px;
            margin: -2px -2px -2px -1px;
            border-radius: 1px;
        }
                
        QSlider::sub-page:horizontal{
          background:#3396DA;
        }
        """)
        self.__init_icons()
        self.update_icon(self.openButton, "open")
        self.update_icon(self.playButton, "play")
        self.update_icon(self.snapshotButton, "snapshot")
        self.update_icon(self.startButton, "start")
        self.update_icon(self.endButton, "end")
        self.update_icon(self.autoSnapshotButton, "auto")
        self.update_icon(self.imageStitchingButton, "stitching")

    def __init_icons(self):
        player = os.path.join("windows", "player")
        self.add_icon("open.svg", player)
        self.add_icon("play.svg", player)
        self.add_icon("pause.svg", player)
        self.add_icon("snapshot.svg", player)
        self.add_icon("start.svg", player)
        self.add_icon("end.svg", player)
        self.add_icon("auto.svg", player)
        self.add_icon("stitching.svg", player)

