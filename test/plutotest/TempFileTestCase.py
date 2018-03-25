import inspect
import shutil
import unittest

import os

from pluto.common.utils import TempFileUtil


class TempFileTestCase(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.realpath(
            os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '../files/'))
        self.__temp_files = []

    def tearDown(self):
        for filename in self.__temp_files:
            if os.path.isfile(filename):
                os.remove(filename)
            elif os.path.isdir(filename):
                shutil.rmtree(filename)

    def get_temp_file(self, prefix="snapshot_unit_test_", suffix=".jpg", delete=True):
        temp_file = TempFileUtil.get_temp_file(prefix=prefix, suffix=suffix)
        if delete:
            self.__temp_files.append(temp_file)
        else:
            print('DEBUG: Generate temp file:', temp_file)
        return temp_file
