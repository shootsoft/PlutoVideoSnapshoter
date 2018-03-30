# -*- coding: utf-8 -*-

import inspect
import shutil
import tempfile
import unittest

import os

from pluto.common.utils import TempFileUtil
from pluto.common.media.snapshot import Snapshot


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.snapshot = Snapshot()
        self.resource = os.path.realpath(
            os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '../../../files'))
        self.video_file = self.resource + "/video/A Message from President-Elect Donald J- Trump.mp4"
        self.temp_files = []

    def tearDown(self):
        for filename in self.temp_files:
            if os.path.isfile(filename):
                os.remove(filename)
            elif os.path.isdir(filename):
                shutil.rmtree(filename)

    def test_detect_srt(self):
        self.assertIsNone(Snapshot.detect_srt("test.avi"))
        self.assertEqual(self.resource + "/video/A Message from President-Elect Donald J- Trump.mp4.srt",
                         Snapshot.detect_srt(self.video_file))
        self.assertEqual(self.resource + "/empty/video.srt",
                         Snapshot.detect_srt(self.resource + "/empty/video.mp4"))

    def test_load_video_nosrt(self):
        video_file = self.resource + "/empty/nosrt.avi"
        self.snapshot.load_video(video_file)
        self.assertEqual("", self.snapshot.srt_file)
        self.assertEqual([], self.snapshot.srt_subs)
        self.assertEqual(video_file, self.snapshot.video_file)

    def test_load_video_no_srt(self):
        video_file = self.resource + "/empty/nosrt.avi"
        temp_file = self.get_temp_file()
        self.snapshot.load_video(video_file)
        self.assertEqual("", self.snapshot.srt_file)
        self.assertEqual([], self.snapshot.srt_subs)
        self.assertEqual(video_file, self.snapshot.video_file)
        self.assertEqual(0, self.snapshot.estimate(0, 100))
        self.assertFalse(self.snapshot.snapshot(10, temp_file))

    def test_load_estimate(self):
        self.snapshot.load_video(self.video_file)
        self.assertIsNotNone(self.snapshot.srt_file)
        self.assertEqual(62, self.snapshot.estimate())
        self.assertEqual(11, self.snapshot.estimate(13000, 45000))

    def test_load_snapshot(self):
        self.snapshot.load_video(self.video_file)
        temp_file = self.get_temp_file()
        self.assertTrue(self.snapshot.snapshot(13000, temp_file))
        file_info1 = os.stat(temp_file)
        self.assertTrue(file_info1.st_size > 50000)

    def test_load_snapshot_failed(self):
        self.snapshot.load_video(self.video_file)
        with self.assertRaises(Exception) as context:
            self.snapshot.snapshot(13000, "test")

    def test_load_snapshot_range(self):
        self.snapshot.load_video(self.video_file)
        dir = self.get_temp_dir()
        total = self.snapshot.estimate(13000, 20000)
        self.assertFalse(self.snapshot.snapshot_range(dir, 13000, 20000, self.show_progress, self.show_complete))
        print(os.listdir(dir))
        self.assertEqual(total, len(os.listdir(dir)))

    def test_load_snapshot_range_failed(self):
        self.snapshot.load_video(self.video_file)
        dir = self.get_temp_dir()
        self.assertFalse(self.snapshot.snapshot_range(dir, 2000, 1000, self.show_progress, self.show_complete))
        self.assertEqual(0, len(os.listdir(dir)))

    def show_progress(self, total, current, position, output_file, output_result):
        print("total=%s, current=%s, position=%s, output_file=%s, output_result=%s" % (
            total, current, position, output_file, output_result))
        self.assertTrue(output_result)

    def show_complete(self, total, success):
        self.assertEqual(total, success)

    def get_temp_file(self):
        temp_file = TempFileUtil.get_temp_file(suffix=".jpg", prefix="snapshot_unit_test_")
        self.temp_files.append(temp_file)
        return temp_file

    def get_temp_dir(self):
        temp_dir = tempfile.mkdtemp(prefix="snapshot_")
        self.temp_files.append(temp_dir)
        return temp_dir


if __name__ == '__main__':
    unittest.main()
