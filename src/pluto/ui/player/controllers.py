# -*- coding: utf-8 -*-

import os
import traceback

from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QSound
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication

from pluto.common.utils import TimeUtil
from pluto.common.media.snapshot import Snapshot
from pluto.ui.player.models import SnapshotModel
from pluto.ui.player.views import PlayerWindow

from pluto.ui.qt.mvc.controllers import Controller
from pluto.ui.qt.qtutils import QtUtil


class PlayerController(Controller):
    def __init__(self, router):
        super(PlayerController, self).__init__(router, PlayerWindow())
        self.model = SnapshotModel()
        self.snapshot = Snapshot()
        self.snapshotSound = QSound(QtUtil.resource_path(os.path.join("windows", "player", "snapshot.wav")))
        self.__bind(self.view)

    def __bind(self, view):
        view.openButton.clicked.connect(self.on_open)
        view.playButton.clicked.connect(self.on_play)
        view.snapshotButton.clicked.connect(self.on_snapshot)
        view.videoBackgroundWidget.mouseReleaseEvent = self.on_video_clicked
        view.videoWidget.mouseReleaseEvent = self.on_video_clicked

        view.outputButton.clicked.connect(self.on_set_output)
        view.subtitleSelectButton.clicked.connect(self.on_set_subtitle)

        view.startButton.clicked.connect(self.on_set_start)
        view.endButton.clicked.connect(self.on_set_end)
        view.autoSnapshotButton.clicked.connect(self.on_run_snapshots)
        view.imageStitchingButton.clicked.connect(self.on_stitch_snapshots)

        self.view.mediaPlayer.stateChanged.connect(self.on_media_state_changed)
        self.view.mediaPlayer.positionChanged.connect(self.on_position_changed)
        self.view.mediaPlayer.durationChanged.connect(self.on_duration_changed)
        self.view.mediaPositionSlider.sliderMoved.connect(self.on_set_position)

        self.view.videoBackgroundWidget.resizeEvent = self.on_video_resize

    def on_open(self):
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open Video", QDir.homePath(),
                                                   filter="*.mp4;*.avi;*.mpeg;*.mpg;*.mov;*.m4v;*.mtk")
        if file_name != '':
            if not self.snapshot.load_video(file_name):
                QMessageBox.warning(self.view, 'Error', "Can't open this file.")
                return
            self.model = SnapshotModel()
            self.model.filename = file_name
            self.view.outputLineEdit.setText(self.model.output)
            self.view.playButton.setEnabled(True)
            self.view.snapshotButton.setEnabled(True)
            self.view.subtitleSelectButton.setEnabled(True)
            self.view.startButton.setEnabled(True)
            self.view.endButton.setEnabled(True)
            self.view.outputButton.setEnabled(True)
            if self.snapshot.srt_file:
                self.model.subtitle = self.snapshot.srt_file
                self.view.subtitleLineEdit.setText(self.snapshot.srt_file)
                self.view.autoSnapshotButton.setEnabled(True)
            self.set_video(file_name, self.snapshot.width, self.snapshot.height)

    def on_video_clicked(self, *event):
        if self.model.filename:
            self.on_play()
        else:
            self.on_open()

    def on_play(self, ):
        self.view.mediaPositionSlider.setEnabled(True)
        if self.model.isPlaying:
            self.view.mediaPlayer.pause()
            self.view.update_icon(self.view.playButton, "play")
        else:
            self.view.mediaPlayer.play()
            self.view.update_icon(self.view.playButton, "pause")
        self.model.isPlaying = not self.model.isPlaying
        self.view.videoWidget.show()

    def on_set_output(self):
        folder = QFileDialog.getExistingDirectory(self.view, "Select image output path", self.model.output)
        if folder:
            self.model.output = folder
            self.view.outputLineEdit.setText(self.model.output)

    def on_set_subtitle(self):
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open Subtitle", QDir.homePath(),
                                                   filter="*.srt")
        if file_name != '':
            self.snapshot.load_srt(file_name)
            self.view.subtitleLineEdit.setText(file_name)
            self.model.subtitle = file_name
            self.view.autoSnapshotButton.setEnabled(True)

    def on_stitch_snapshots(self):
        if self.model.isPlaying:
            self.on_play()
        self.go('image')

    def set_video(self, file_name, width, height):
        self.view.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
        QtUtil.central(self.view.videoWidget, self.view.videoBackgroundWidget, width, height, 2, 2)
        self.on_play()

    def on_media_state_changed(self, state):
        # TODO: find a method to update view instead of these tricks
        # After pause, the video will re-scale to original size, this is used to fix this.
        QtUtil.central(self.view.videoWidget, self.view.videoBackgroundWidget,
                       self.snapshot.width, self.snapshot.height, 2, 2)
        if state == 0:
            # TODO: find a method to update view instead of these tricks
            self.view.videoWidget.hide()
            self.model.isPlaying = False
            self.view.update_icon(self.view.playButton, "play")
            self.view.mediaPositionSlider.hide()
            self.view.mediaPositionSlider.setValue(0)
            self.view.mediaPositionSlider.show()
        elif state == QMediaPlayer.PausedState:
            self.view.update_icon(self.view.playButton, "play")
        else:
            self.view.update_icon(self.view.playButton, "pause")

    def on_video_resize(self, event):
        QtUtil.central(self.view.videoWidget, self.view.videoBackgroundWidget,
                       self.snapshot.width, self.snapshot.height)

    def on_position_changed(self, position):
        # TODO: find a method to update view instead of these tricks
        QtUtil.central(self.view.videoWidget, self.view.videoBackgroundWidget,
                       self.snapshot.width, self.snapshot.height)
        self.view.mediaPositionSlider.setValue(position)
        self.view.progressLabel.setText(TimeUtil.format_ms(position))

    def on_duration_changed(self, duration):
        print(duration)
        self.view.mediaPositionSlider.setRange(0, duration)
        self.model.end = duration
        self.view.endLabel.setText(TimeUtil.format_ms(duration))

    def on_set_position(self, position):
        self.view.mediaPlayer.setPosition(position)

    def on_handle_error(self, error):
        self.view.playButton.setEnabled(False)
        self.view.snapshotButton.setEnabled(False)
        self.view.startButton.setEnabled(False)
        self.view.endButton.setEnabled(False)
        self.view.outputButton.setEnabled(False)
        self.view.subtitleButton.setEnabled(False)
        self.view.runTaskButton(False)
        self.view.messageLabel.setText("Error: " + self.view.mediaPlayer.errorString())
        print(error)

    def on_snapshot(self):
        position = self.view.mediaPlayer.position()
        output_file = os.path.join(self.model.output, self.model.file + "_manual_%s.jpg" %
                                   TimeUtil.format_ms(position).replace(":", "_"))
        # print(output_file)
        try:
            if self.snapshot.snapshot(position, output_file):
                self.snapshotSound.play()
                self.router.notify('snapshot', output_file)
                self.view.messageLabel.setText("Saved " + output_file)
        except:
            traceback.print_exc()
            QMessageBox.warning(self.view, 'Error', 'Snapshot failed.')

    def on_set_start(self):
        self.model.start = self.view.mediaPlayer.position()
        self.view.startLabel.setText(TimeUtil.format_ms(self.model.start))

    def on_set_end(self):
        self.model.end = self.view.mediaPlayer.position()
        self.view.endLabel.setText(TimeUtil.format_ms(self.model.end))

    def on_run_snapshots(self):
        if self.view.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.on_play()

        count = self.snapshot.estimate(self.model.start, self.model.end)
        quit_msg = "Are you sure you want to run auto snapshot (start %s ~ end %s )?\n" \
                   "Image count estimation %s" % (TimeUtil.format_ms(self.model.start),
                                                  TimeUtil.format_ms(self.model.end), count)
        reply = QMessageBox.question(self.view, 'Run Auto Snapshot', quit_msg, QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.lock_ui(False)
            self.model.task_progress = 0
            try:
                self.snapshot.snapshot_range(self.model.output, self.model.start, self.model.end,
                                             self.show_progress, self.show_complete)
            except:
                traceback.print_exc()
                QMessageBox.warning(self.view, 'Error', 'Snapshot failed.')
            self.lock_ui(True)

    def show_progress(self, total, current, position, output_file, output_result):
        QApplication.processEvents()
        self.router.notify('snapshot', output_file)
        percentage = int(current * 100 / total)
        if percentage != self.model.task_progress:
            self.model.task_progress = percentage
            self.view.messageLabel.setText("Progress %s%%" % percentage)
        print("total=%s, current=%s, position=%s, output_file=%s, output_result=%s" % (
            total, current, position, output_file, output_result))

    def show_complete(self, total, success):
        self.view.messageLabel.setText("Progress 100%%, all done, %s files expected, %s files saved" % (total, success))

    def lock_ui(self, locked_status):
        self.view.playButton.setEnabled(locked_status)
        self.view.openButton.setEnabled(locked_status)
        self.view.outputButton.setEnabled(locked_status)
        self.view.subtitleSelectButton.setEnabled(locked_status)
        self.view.snapshotButton.setEnabled(locked_status)
        self.view.startButton.setEnabled(locked_status)
        self.view.endButton.setEnabled(locked_status)
        self.view.autoSnapshotButton.setEnabled(locked_status)
        self.view.mediaPositionSlider.setEnabled(locked_status)
        self.view.imageStitchingButton.setEnabled(locked_status)
