# -*- coding: utf-8 -*-

import os

import cv2
import numpy as np


class ImageModel(object):
    def __init__(self, image_file=None):
        self.image_file = ""
        # self.image = None
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
