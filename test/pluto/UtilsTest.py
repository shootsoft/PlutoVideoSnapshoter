import inspect
import shutil
import tempfile
import unittest

import os
from collections import namedtuple

from PIL import Image

from pluto.utils import SizeUtil, TimeUtil, SrtUtil, ImageUtil, TempFileUtil


class SizeUtilTest(unittest.TestCase):
    def test_fit(self):
        new_size = SizeUtil.fit(1920, 1080, 600, 400)
        self.assertEqual(600, new_size.width)
        self.assertEqual(337, new_size.height)

        new_size = SizeUtil.fit(1920, 2392, 500, 200)
        self.assertEqual(160, new_size.width)
        self.assertEqual(200, new_size.height)

        new_size = SizeUtil.fit(10, 20, 500, 200)
        self.assertEqual(100, new_size.width)
        self.assertEqual(200, new_size.height)

    def test_fit_zero(self):
        new_size = SizeUtil.fit(0, 0, 600, 400)
        self.assertEqual(0, new_size.width)
        self.assertEqual(0, new_size.height)

        new_size = SizeUtil.fit(10, 10, 0, 0)
        self.assertEqual(0, new_size.width)
        self.assertEqual(0, new_size.height)


class TimeUtilTest(unittest.TestCase):
    def test_format_ms(self):
        time_in_ms = 10120
        self.assertEqual("00:00:10.120", TimeUtil.format_ms(time_in_ms))

    def test_parse_ms(self):
        self.assertEqual(5, TimeUtil.parse_ms("00:00:00,5"))
        self.assertEqual(10005, TimeUtil.parse_ms("00:00:10,5"))
        self.assertEqual(10005, TimeUtil.parse_ms("00:00:10.5"))
        self.assertEqual(1005, TimeUtil.parse_ms("00:00:1,5"))
        self.assertEqual(1000, TimeUtil.parse_ms("00:00:1"))

    def test_parse_ms_failed(self):
        self.assertRaises(ValueError, TimeUtil.parse_ms, "00:00")


class SrtUtilTest(unittest.TestCase):
    def test_parse_srt(self):
        subs = SrtUtil.parse_srt(os.path.realpath(
            os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '../files/test.srt')))
        self.assertEqual(3, len(subs))
        self.assertEqual('the transcript for the whole video is unleashed.', subs[1].content[0])


class ImageUtilTest(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for filename in self.temp_files:
            if os.path.isfile(filename):
                os.remove(filename)
            elif os.path.isdir(filename):
                shutil.rmtree(filename)

    def test_concat(self):
        base_dir = os.path.realpath(
            os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '../files'))
        Img = namedtuple('Img', 'image_file width height up down')
        images = [
            Img(os.path.join(base_dir, 'images/1.jpg'), 640, 360, 268, 320),
            Img(os.path.join(base_dir, 'images/2.jpg'), 640, 360, 268, 320),
        ]
        temp = self.get_temp_file()
        self.assertTrue(ImageUtil.vertical_stitch(images, temp))
        self.assertEqual(Image.open(os.path.join(base_dir, 'images/expected.jpg')), Image.open(temp))

    def get_temp_file(self):
        temp_file = TempFileUtil.get_temp_file(suffix=".jpg", prefix="snapshot_unit_test_")
        self.temp_files.append(temp_file)
        return temp_file


if __name__ == '__main__':
    unittest.main()
