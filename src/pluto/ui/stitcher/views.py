# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QAction, QMenu)

from pluto.ui.qt.mvc.views import View
from pluto.ui.stitcher.models import ViewModel


class ImageStitchingWindow(View):
    def __init__(self):
        super(ImageStitchingWindow, self).__init__(ui_file="image_stitching_window.ui")
        self.imageListWidget.setIconSize(QSize(96, 96))
        self.imageListWidget.resize(self.width() * 0.36, self.imageListWidget.height())
        self.upImageLabel.setGeometry(0, 0, 0, 0)
        self.upImageLabel.setStyleSheet("QLabel { background-color : rgba(0,0,0,.8); opacity:0.3;}")
        self.upImageLabel.setText("")
        self.downImageLabel.setGeometry(0, 0, 0, 0)
        self.downImageLabel.setStyleSheet("QLabel { background-color : rgba(0,0,0,.8); opacity:0.3;}")
        self.downImageLabel.setText("")
        self.zoomInButton.hide()
        self.zoomOutButton.hide()
        self.downVerticalSlider.setValue(0)
        self.__init_icons()
        self.update_icon(self.goBackButton, "player")
        self.update_icon(self.autoDetectButton, "magic")
        self.update_icon(self.addButton, "add")
        self.update_icon(self.removeButton, "remove")
        self.update_icon(self.saveButton, "save")
        self.__init_context_menu()
        self.model = ViewModel()
        self.update_view()

        self.upVerticalSlider.setStyleSheet("""
            QSlider::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 0px solid #777;
                height: 16px;
                margin: -2px -2px -2px -2px;
                border-radius: 1px;
            }

            QSlider::sub-page:vertical{
              background:#3396DA;
            }
            """)
        self.downVerticalSlider.setStyleSheet("""
            QSlider::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 0px solid #5c5c5c;
                height: 16px;
                margin: -2px -2px -2px -2px;
                border-radius: 1px;
            }
    
            QSlider::add-page:vertical{
              background:#3396DA;
            }
            """)

    def __init_context_menu(self):
        self.contextMenu = QMenu()
        self.addAction = QAction("Add images", self)
        self.removeSelectedAction = QAction("Remove selected", self)
        self.autoDetectSelectedAction = QAction("Magic", self)
        self.update_icon(self.autoDetectSelectedAction, "magic")
        self.previewSelectedAction = QAction("Preview selected", self)
        self.previewAllAction = QAction("Preview all", self)
        self.saveSelectedAction = QAction("Save selected", self)
        self.saveAllAction = QAction("Save all", self)

        self.contextMenu.addAction(self.addAction)
        self.contextMenu.addAction(self.removeSelectedAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.autoDetectSelectedAction)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.previewSelectedAction)
        self.contextMenu.addAction(self.previewAllAction)
        self.contextMenu.addAction(self.saveSelectedAction)
        self.contextMenu.addAction(self.saveAllAction)
        self.imageListWidget.customContextMenuRequested.connect(self.on_open_menu)

    def on_open_menu(self, position):
        self.contextMenu.exec_(self.imageListWidget.mapToGlobal(position))

    def __init_icons(self):
        folder = os.path.join("windows", "stitching")
        self.add_icon("player.svg", folder)
        self.add_icon("add.svg", folder)
        self.add_icon("remove.svg", folder)
        self.add_icon("magic.svg", folder)
        self.add_icon("save.svg", folder)

    def update_view(self):
        self.model.items_count = self.imageListWidget.count()
        self.model.select_items_count = len(self.imageListWidget.selectedItems())

        status = self.model.items_count > 0
        self.autoDetectSelectedAction.setEnabled(status)
        self.autoDetectButton.setEnabled(status)
        self.saveButton.setEnabled(status)
        self.saveAllAction.setEnabled(status)
        self.previewAllAction.setEnabled(status)

        select_status = self.model.select_items_count > 0
        self.removeButton.setEnabled(select_status)
        self.removeSelectedAction.setEnabled(select_status)
        self.saveSelectedAction.setEnabled(select_status)
        self.previewSelectedAction.setEnabled(select_status)

        if self.model.preview:
            self.addButton.hide()
            self.removeButton.hide()
            self.autoDetectButton.hide()
        else:
            self.addButton.show()
            self.removeButton.show()
            self.autoDetectButton.show()
