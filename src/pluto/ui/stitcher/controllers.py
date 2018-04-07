# -*- coding: utf-8 -*-

import os
import traceback

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFileDialog, QMessageBox, QApplication)

from pluto.common.media.TextDetector import TextDetector
from pluto.common.utils import ImageUtil, TempFileUtil
from pluto.ui.qt.ListWidgetItem import ListWidgetItem
from pluto.ui.qt.mvc.controllers import Controller
from pluto.ui.qt.qtutils import QtUtil
from pluto.ui.stitcher.models import ImageModel
from pluto.ui.stitcher.views import ImageStitchingWindow


class ImageStitchingController(Controller):
    def __init__(self, router):
        super(ImageStitchingController, self).__init__(router, ImageStitchingWindow())
        self.current_image = None
        self.preview_image_file = None
        self.preview_mode = 0
        self.router.subscribe('snapshot', self)
        self.files = []
        self.text_detector = TextDetector()
        self.__bind(self.view)

    def __bind(self, view):
        view.goBackButton.clicked.connect(self.on_go_back)
        view.addButton.clicked.connect(self.on_add_item)
        view.autoDetectButton.clicked.connect(self.on_auto_detect)
        view.removeButton.clicked.connect(self.on_remove_item)
        view.saveButton.clicked.connect(self.on_save)
        view.imageListWidget.itemSelectionChanged.connect(self.on_item_selected)
        view.upVerticalSlider.sliderMoved.connect(self.on_up_moved)
        view.downVerticalSlider.sliderMoved.connect(self.on_down_moved)
        view.tabWidget.tabBarClicked.connect(self.on_tab_clicked)
        view.imageWidget.resizeEvent = self.on_item_preview_resize
        view.previewWidget.resizeEvent = self.on_output_preview_resize
        view.addAction.triggered.connect(self.on_add_item)
        view.autoDetectSelectedAction.triggered.connect(self.on_auto_detect)
        view.removeSelectedAction.triggered.connect(self.on_remove_item)
        view.previewSelectedAction.triggered.connect(self.on_preview_selected)
        view.previewAllAction.triggered.connect(self.on_preview_all)
        view.saveSelectedAction.triggered.connect(self.on_save_selected)
        view.saveAllAction.triggered.connect(self.on_save_all)

    def show(self):
        super(ImageStitchingController, self).show()
        if len(self.files) > 0:
            for image in self.files:
                self.add_image(image)
            self.files = []

    def notify(self, topic, message):
        if topic == 'snapshot':
            self.files.append(message)

    def on_go_back(self):
        self.go('player')

    def on_add_item(self):
        file_names, _ = QFileDialog.getOpenFileNames(self.view, "Open Images", QDir.homePath(),
                                                     filter="*.jpg;*.jpeg;*.png")
        if file_names:
            for image in file_names:
                self.add_image(image)
            self.view.statusBar().showMessage("%s images added." % len(file_names))

    def on_remove_item(self):
        items = self.view.imageListWidget.selectedItems()
        if len(items) == 0:
            return
        result = QMessageBox.question(self.view, 'Run Auto Snapshort', 'Remove selected [%s] items?' % len(items),
                                      QMessageBox.Yes, QMessageBox.No)
        if result == QMessageBox.Yes:
            for item in items:
                index = self.view.imageListWidget.indexFromItem(item)
                self.view.imageListWidget.takeItem(index.row())
            self.view.imageListWidget.repaint()
            self.view.statusBar().showMessage('Removed %s images.' % len(items))
            if self.view.imageListWidget.count() == 0:
                self.view.saveButton.setEnabled(False)
                self.view.autoDetectButton.setEnabled(False)

    def add_image(self, image_file):
        try:
            image = ImageModel(image_file)
            item = ListWidgetItem()
            icon = QIcon()
            icon.addFile(image_file)
            item.setTextAlignment(1)
            item.setIcon(icon)
            item.setData(Qt.DisplayRole, str(image))
            item.setData(Qt.StatusTipRole, image_file)
            item.set_storage(image)
            self.view.imageListWidget.addItem(item)
            if not self.view.saveButton.isEnabled():
                self.view.saveButton.setEnabled(True)
                self.view.autoDetectButton.setEnabled(True)
        except:
            traceback.print_exc()

    def on_item_selected(self):
        items = self.view.imageListWidget.selectedItems()
        if len(items) == 0:
            self.view.upVerticalSlider.setValue(0)
            self.view.upVerticalSlider.setEnabled(False)
            self.view.downVerticalSlider.setEnabled(False)
            self.view.downVerticalSlider.setValue(0)
            self.view.imageLabel.hide()
            self.view.upImageLabel.hide()
            self.view.downImageLabel.hide()
            self.view.removeButton.setEnabled(False)
            self.current_image = None
            self.view.statusBar().showMessage('')
        else:
            item = items[0]
            image = item.get_storage()
            self.current_image = image

            self.render_preview()
            self.view.imageLabel.show()
            self.view.upImageLabel.show()
            self.view.downImageLabel.show()
            self.view.removeButton.setEnabled(True)
            self.view.upVerticalSlider.setEnabled(True)
            self.view.downVerticalSlider.setEnabled(True)
            self.view.statusBar().showMessage("%s images selected." % len(items))

    def render_preview(self):
        image = self.current_image
        if image is None:
            return
        QtUtil.preview_image(image.image_file, self.view.imageLabel, self.view.imageWidget)
        self.set_image_up_shade(image)
        self.set_image_down_shade(image)
        self.view.upVerticalSlider.setRange(0, image.height)
        self.view.downVerticalSlider.setRange(0, image.height)
        self.view.upVerticalSlider.setValue(image.up)
        self.view.downVerticalSlider.setValue(image.height - image.down)

    def set_image_up_shade(self, image):
        height = int(self.view.imageLabel.height() * (image.up * 1.0 / image.height))
        self.view.upImageLabel.setGeometry(self.view.imageLabel.x(), self.view.imageLabel.y(),
                                           self.view.imageLabel.width(),
                                           height)
        # print 'up x, y, width, height', self.view.upImageLabel.geometry()

    def set_image_down_shade(self, image):
        height = int(self.view.imageWidget.height() * ((image.height - image.down) * 1.0 / image.height))
        self.view.downImageLabel.setGeometry(self.view.imageLabel.x(),
                                             self.view.imageLabel.y() + self.view.imageLabel.height() - height,
                                             self.view.imageLabel.width(), height)
        # print 'down x, y, width, height', self.view.downImageLabel.geometry()

    def on_up_moved(self, position):
        updated = False
        for item in self.view.imageListWidget.selectedItems():
            image = item.get_storage()
            if position < image.down:
                image.up = position
                item.setData(0, str(image))
                if not updated:
                    updated = True
                    self.set_image_up_shade(image)

            else:
                self.view.upVerticalSlider.setValue(image.up)
                break

    def on_down_moved(self, position):
        updated = False
        for item in self.view.imageListWidget.selectedItems():
            image = item.get_storage()
            val = image.height - position
            if val > image.up:
                image.down = val
                item.setData(0, str(image))
                if not updated:
                    updated = True
                    self.set_image_down_shade(image)
            else:
                self.view.downVerticalSlider.setValue(image.height - image.down)
                break

    def on_save(self):
        filename, _ = QFileDialog.getSaveFileName(self.view, "Save Image", QDir.homePath(),
                                                  filter="*.jpg")
        if filename:
            images = self.get_images(self.preview_mode)
            ImageUtil.vertical_stitch(images, filename)
            self.view.statusBar().showMessage('Image %s saved.' % filename)
        else:
            self.view.statusBar().showMessage('Save cancelled.')

    def get_images(self, mode=0):
        images = []
        if mode == 0:
            for i in range(self.view.imageListWidget.count()):
                item = self.view.imageListWidget.item(i)
                images.append(item.get_storage())
        else:
            for item in self.view.imageListWidget.selectedItems():
                images.append(item.get_storage())

        return images

    def on_item_preview_resize(self, event):
        if self.current_image is not None:
            QtUtil.central(self.view.imageLabel, self.view.imageWidget,
                           self.current_image.width, self.current_image.height)
            self.set_image_up_shade(self.current_image)
            self.set_image_down_shade(self.current_image)

    def on_tab_clicked(self, index):
        is_preview = index == 1
        self.view.statusBar().showMessage("Preview image." if is_preview else '')
        if is_preview:
            self.render_stitching_preview()
        else:
            self.view.addButton.show()
            self.view.removeButton.show()
            self.view.autoDetectButton.show()

    def render_stitching_preview(self):
        images = self.get_images(self.preview_mode)
        if len(images) > 0:
            temp_file = TempFileUtil.get_temp_file(prefix="snapshot_preview_", suffix=".jpg")
            self.preview_image_file = ImageUtil.vertical_stitch(images, temp_file)
            QtUtil.preview_image(temp_file, self.view.previewLabel, self.view.previewWidget)
            os.remove(temp_file)
        else:
            self.preview_image_file = None
            self.view.previewLabel.clear()
        self.view.addButton.hide()
        self.view.removeButton.hide()
        self.view.autoDetectButton.hide()

    def on_output_preview_resize(self, event):
        if self.preview_image_file is not None:
            QtUtil.central(self.view.previewLabel, self.view.previewWidget,
                           self.preview_image_file.width, self.preview_image_file.height)

    def on_preview_selected(self):
        self.view.tabWidget.setCurrentIndex(1)
        self.preview_mode = 1
        self.on_tab_clicked(1)

    def on_preview_all(self):
        self.view.tabWidget.setCurrentIndex(1)
        self.preview_mode = 0
        self.on_tab_clicked(1)

    def on_save_selected(self):
        self.preview_mode = 1
        self.on_save()

    def on_save_all(self):
        self.preview_mode = 0
        self.on_save()

    def on_auto_detect(self):
        message = "Auto detect subtitle positions for "
        items = []
        skip_first = False
        if len(self.view.imageListWidget.selectedItems()) > 0:
            message += "selected images?"
            items = self.view.imageListWidget.selectedItems()
        else:
            message += "all images (except the head image)?"
            for i in range(self.view.imageListWidget.count()):
                items.append(self.view.imageListWidget.item(i))
            skip_first = True
        reply = QMessageBox.question(self.view, 'Auto detect', message, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.view.setEnabled(False)
            self.do_auto_detect(items, skip_first)
            QApplication.processEvents()
            self.view.setEnabled(True)

    def do_auto_detect(self, items, skip_first=False):
        start = 1 if skip_first else 0
        for i in range(start, len(items)):
            img = items[i].get_storage()
            img.up, img.down = self.text_detector.detect_subtitle_range(img.image_file)
            # items[i].setData(0, str(img))
            items[i].refresh_ui()
        self.render_preview()
        self.view.statusBar().showMessage("Please preview final image.")