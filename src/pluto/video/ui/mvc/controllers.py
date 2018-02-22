import os

import cv2
from PyQt5.QtCore import QDir, QUrl, QRunnable, pyqtSlot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (QApplication, QFileDialog, QStyle, QMessageBox)

from pluto.utils import TimeUtil, SrtUtil
from pluto.video.snapshot import Snapshot
from pluto.video.ui.mvc.models import Task


class MainController(object):
    def __init__(self, app, view=None):
        self.app = app
        self.view = view
        self.model = Task()
        self.snapshot = Snapshot()

    def set_view(self, view):
        self.view = view

    def on_open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open Video", QDir.homePath(),
                                                   filter="*.mp4;*.avi;*.mpeg;*.mpg")
        if file_name != '':
            self.model = Task()
            self.model.filename = file_name
            self.view.outputLineEdit.setText(self.model.output)
            self.view.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.view.playButton.setEnabled(True)
            self.view.snapshotButton.setEnabled(True)
            self.view.subtitleButton.setEnabled(True)
            self.view.startButton.setEnabled(True)
            self.view.endButton.setEnabled(True)
            self.view.outputButton.setEnabled(True)
            self.snapshot.load_video(file_name)
            if self.snapshot.srt_file:
                self.model.subtitle = self.snapshot.srt_file
                self.view.subTitleLabel.setText(self.snapshot.srt_file)
                self.view.runTaskButton.setEnabled(True)

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
            self.view.subTitleLabel.setText(file_name)
            self.model.subtitle = file_name
            self.view.runTaskButton.setEnabled(True)

    def on_play(self):
        if self.view.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.view.mediaPlayer.pause()
        else:
            self.view.mediaPlayer.play()
            height = self.view.frameGeometry().height() - 200
            self.view.videoWidget.setGeometry(10, 10, height * 1.778, height)

    def on_media_state_changed(self, state):
        if self.view.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.view.playButton.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.view.playButton.setIcon(
                self.view.style().standardIcon(QStyle.SP_MediaPlay))

    def on_position_changed(self, position):
        self.view.positionSlider.setValue(position)
        self.view.statusLabel.setText("Progress: " + TimeUtil.format_ms(position))

    def on_duration_changed(self, duration):
        self.view.positionSlider.setRange(0, duration)
        self.model.end = duration
        self.view.endLabel.setText(TimeUtil.format_ms(duration))

    def on_set_position(self, position):
        self.view.mediaPlayer.setPosition(position)

    def on_handle_error(self):
        self.view.playButton.setEnabled(False)
        self.view.snapshotButton.setEnabled(False)
        self.view.startButton.setEnabled(False)
        self.view.endButton.setEnabled(False)
        self.view.outputButton.setEnabled(False)
        self.view.subtitleButton.setEnabled(False)
        self.view.runTaskButton(False)
        self.view.statusLabel.setText("Error: " + self.view.mediaPlayer.errorString())

    def on_snapshot(self):
        position = self.view.mediaPlayer.position()
        output_file = os.path.join(self.model.output, self.model.file + "_%d.jpg" % position)
        try:
            if self.snapshot.snapshot(position, output_file):
                self.view.statusLabel.setText("Saved " + output_file)
        except:
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
        reply = QMessageBox.question(self.view, 'Run Auto Snapshort', quit_msg, QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.lock_ui(False)
            self.model.task_progress = 0
            try:
                self.snapshot.snapshot_range(self.model.output, self.model.start, self.model.end,
                                             self.show_progress, self.show_complete)
            except:
                QMessageBox.warning(self.view, 'Error', 'Snapshot failed.')

            self.lock_ui(True)
        else:
            print 'Task cancelled.'

    def show_progress(self, total, current, position, output_file, output_result):
        QApplication.processEvents()
        percentage = current * 100 / total
        if percentage != self.model.task_progress:
            self.model.task_progress = percentage
            self.view.statusLabel.setText("Progress %s%%" % percentage)
        print "total=%s, current=%s, position=%s, output_file=%s, output_result=%s" % (
            total, current, position, output_file, output_result)

    def show_complete(self, total, success):
        self.view.statusLabel.setText("Progress 100%%, all done, %s files expected, %s files saved" % (total, success))

    def lock_ui(self, locked_status):
        self.view.playButton.setEnabled(locked_status)
        self.view.openButton.setEnabled(locked_status)
        self.view.outputButton.setEnabled(locked_status)
        self.view.subtitleButton.setEnabled(locked_status)
        self.view.snapshotButton.setEnabled(locked_status)
        self.view.startButton.setEnabled(locked_status)
        self.view.endButton.setEnabled(locked_status)
        self.view.runTaskButton.setEnabled(locked_status)
        self.view.positionSlider.setEnabled(locked_status)
