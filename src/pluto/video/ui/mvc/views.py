# -*- coding: utf-8 -*-

import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QHBoxLayout, QLabel,
                             QSizePolicy, QSlider, QStyle, QVBoxLayout,
                             QGridLayout, QLineEdit)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton


class VideoWindow(QMainWindow):
    def __init__(self, ctrl=None, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Pluto Video Snapshotor")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget()

        self.openButton = QPushButton()
        self.openButton.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.openButton.setToolTip("Open a video")

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.snapshotButton = QPushButton()
        self.snapshotButton.setEnabled(False)
        self.snapshotButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.snapshotButton.setToolTip("Take a snapshot of current position")

        self.outputButton = QPushButton()
        self.outputButton.setEnabled(False)
        self.outputButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.outputButton.setToolTip("Select output path")

        self.outputLineEdit = QLineEdit()
        self.outputLineEdit.setReadOnly(True)

        self.subtitleButton = QPushButton()
        self.subtitleButton.setEnabled(False)
        self.subtitleButton.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.subtitleButton.setToolTip("Select subtitles")

        self.subTitleLabel = QLabel("Subtitle file")

        self.startButton = QPushButton()
        self.startButton.setEnabled(False)
        self.startButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.startButton.setToolTip("Set start")

        self.endButton = QPushButton()
        self.endButton.setEnabled(False)
        self.endButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.endButton.setToolTip("Set end")

        self.runTaskButton = QPushButton()
        self.runTaskButton.setEnabled(False)
        self.runTaskButton.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.runTaskButton.setToolTip("Run snapshots")

        self.imageButton = QPushButton()
        self.imageButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.imageButton.setToolTip("Stitch snapshots")

        self.startLabel = QLabel("00:00:00")
        self.endLabel = QLabel("End of video")

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)

        self.statusLabel = QLabel()
        self.statusLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.snapshotButton)
        controlLayout.addWidget(self.positionSlider)

        outputLayout = QGridLayout()
        outputLayout.setContentsMargins(0, 0, 0, 0)
        outputLayout.addWidget(self.outputButton, 0, 0, 1, 1)
        outputLayout.addWidget(self.outputLineEdit, 0, 1, 1, 6)

        outputLayout.addWidget(self.subtitleButton, 1, 0, 1, 1)
        outputLayout.addWidget(self.subTitleLabel, 1, 1, 1, 6)

        outputLayout.addWidget(self.startButton, 2, 0, 1, 1)
        outputLayout.addWidget(self.startLabel, 2, 1, 1, 1)
        outputLayout.addWidget(self.endButton, 2, 2, 1, 1)
        outputLayout.addWidget(self.endLabel, 2, 3, 1, 1)
        outputLayout.addWidget(self.runTaskButton, 2, 4, 1, 1)
        outputLayout.addWidget(self.imageButton, 2, 6, 1, 1)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)
        layout.addLayout(outputLayout)
        layout.addWidget(self.statusLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)

        self.__bind_ctrl(ctrl)

    def __bind_ctrl(self, ctrl):
        """
        Binding events handler (not sure why it doesn't work if I moved this method to controller)
        :param ctrl: the Controller
        :return: void
        """
        ctrl.set_view(self)
        self.playButton.clicked.connect(ctrl.on_play)
        self.openButton.clicked.connect(ctrl.on_open_file)
        self.outputButton.clicked.connect(ctrl.on_set_output)
        self.subtitleButton.clicked.connect(ctrl.on_set_subtitle)
        self.snapshotButton.clicked.connect(ctrl.on_snapshot)
        self.startButton.clicked.connect(ctrl.on_set_start)
        self.endButton.clicked.connect(ctrl.on_set_end)
        self.runTaskButton.clicked.connect(ctrl.on_run_snapshots)
        self.imageButton.clicked.connect(ctrl.on_stitch_snapshots)

        self.positionSlider.sliderMoved.connect(ctrl.on_set_position)
        self.mediaPlayer.stateChanged.connect(ctrl.on_media_state_changed)
        self.mediaPlayer.positionChanged.connect(ctrl.on_position_changed)
        self.mediaPlayer.durationChanged.connect(ctrl.on_duration_changed)
        self.mediaPlayer.error.connect(ctrl.on_handle_error)


class ImageStitchingWindow(QMainWindow):
    def __init__(self):
        super(ImageStitchingWindow, self).__init__()
        ui = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'windows', 'image_stitching_window.ui')
        uic.loadUi(ui, self)
        self.imageListWidget.setIconSize(QSize(96, 96))
        self.imageListWidget.resize(self.width() * 0.67, self.imageListWidget.height())
        self.upImageLabel.setGeometry(0, 0, 0, 0)
        self.upImageLabel.setStyleSheet("QLabel { background-color : rgba(0,0,0,.8); opacity:0.3;}")
        self.downImageLabel.setGeometry(0, 0, 0, 0)
        self.downImageLabel.setStyleSheet("QLabel { background-color : rgba(0,0,0,.8); opacity:0.3;}")
        #self.previewWidget.setStyleSheet("QWidget { background-color : rgba(0,0,0,.8); opacity:0.3;}")
