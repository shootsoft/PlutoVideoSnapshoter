# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np


class SnapshotModel(object):
    def __init__(self):
        self.filename = ""
        self.file = ""
        self.folder = ""
        self.subtitle = ""
        self.start = 0
        self.end = 0
        self.output = ""
        self.isPlaying = False
        self.task_progress = 0

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == 'filename' and value != "":
            self.folder, self.file = os.path.split(value)
            if self.__dict__['output'] == "":
                self.__dict__['output'] = self.folder


class ImageModel(object):
    def __init__(self, image_file=None):
        self.image_file = ""
        #self.image = None
        self.up = 0
        self.down = -1
        self.width = 0
        self.height = 0
        self.name = ""

        if image_file:
            self.set_file(image_file)

    def set_file(self, image_file):
        self.image_file = image_file
        image = cv2.imread(image_file)
        self.height = np.size(image, 0)
        self.width = np.size(image, 1)
        self.up = 0
        self.down = self.height
        self.name = os.path.basename(image_file)

    def __str__(self):
        return "up:%s down:%s %s" % (self.up, self.down, self.name)
