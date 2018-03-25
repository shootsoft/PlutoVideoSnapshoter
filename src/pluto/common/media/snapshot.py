import traceback

import cv2
import os

from pluto.common.utils import SrtUtil


class Snapshot(object):
    def __init__(self):
        self.video_file = ""
        self.video_capture = None
        self.srt_file = ""
        self.srt_subs = []
        self.width = 0
        self.height = 0;

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__initialise()

    def __initialise(self):
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
            self.srt_file = ""
            self.srt_subs = []
            self.video_file = ""

    def load_video(self, video_file):
        self.__initialise()
        self.video_capture = cv2.VideoCapture(video_file)
        self.video_file = video_file
        srt_file = self.detect_srt(video_file)
        if srt_file:
            self.load_srt(srt_file)

        if self.video_capture.isOpened():
            self.width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        return self.video_capture.isOpened()

    @staticmethod
    def detect_srt(video_file):
        srt_files = [video_file + '.srt', os.path.splitext(video_file)[0] + '.srt']
        for str_file in srt_files:
            if os.path.isfile(str_file):
                return str_file

    def load_srt(self, srt_file):
        self.srt_file = srt_file
        self.srt_subs = SrtUtil.parse_srt(srt_file)

    def estimate(self, start=0, end=None):
        count = 0
        if len(self.srt_subs) == 0:
            return count
        if end is None:
            end = self.__default_end()
        for sub in self.srt_subs:
            if sub.start >= start and sub.end <= end:
                count += 1
        return count

    def __default_end(self):
        return self.srt_subs[len(self.srt_subs) - 1].end

    def snapshot(self, position, output_file):
        """
        Take a snapshot for certain position of the video
        :param position: integer
        :param output_file: image name
        :return: True for success
        :raise Exception for cv snapshot failure.
        """
        fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            return False
        duration = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT) * 1000.0 / fps
        progress = position * 1.0 / duration
        if progress < 0 or progress > 1.0:
            return False
        frame_pos = int(progress * self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        success, image = self.video_capture.read()
        if success:
            try:
                dir_path = os.path.dirname(os.path.realpath(output_file))
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                result = cv2.imwrite(output_file, image)
                return result
            except:
                traceback.print_exc()
                raise Exception('Snapshot position %s (frame %s) failed %s' % (position, frame_pos, output_file))

        else:
            raise Exception('Snapshot position %s (frame %s) failed %s' % (position, frame_pos, output_file))

    def snapshot_range(self, output_folder, start=0, end=None, callback_progress=None, callback_complete=None):
        """
        Take snapshots for a given range
        :param output_folder: str output folder
        :param start:
        :param end:
        :param callback_progress: call_back_progress(total, current, position, output_file, output_result)
        :param callback_complete: callback_complete(total, success)
        :return:
        """
        total = self.estimate(start, end)
        if total == 0:
            if callback_complete:
                callback_complete(0, 0)
            return

        if end is None:
            end = self.__default_end()
        current = 0
        success = 0
        for sub in self.srt_subs:
            if sub.start >= start and sub.end <= end:
                current += 1
                position = int((sub.start + sub.end) / 2)
                print("current %s start %s end %s mid %s" % (current, sub.start, sub.end, position))
                output_file = os.path.join(output_folder,
                                           "%s_range_%s.jpg" % (os.path.basename(self.video_file), position))
                output_result = self.snapshot(position, output_file)
                success += 1 if output_result else 0
                if callback_progress:
                    try:
                        callback_progress(total, current, position, output_file, output_result)
                    except:
                        traceback.print_exc()
        if callback_complete:
            callback_complete(total, success)
