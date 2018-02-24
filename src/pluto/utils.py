import tempfile
import time

from itertools import groupby
from collections import namedtuple

import re

from PIL import Image


class SizeUtil(object):
    @staticmethod
    def fit(width, height, max_width, max_height):
        """
        Fit size (width height) into new size
        """
        Size = namedtuple('Size', 'width height')
        if width == 0 or height == 0:
            return Size(0, 0)
        x = max_width * 1.0 / width
        y = max_height * 1.0 / height
        target = x if x < y else y
        return Size(int(width * target), int(height * target))


class TimeUtil(object):
    @staticmethod
    def format_ms(ms_time):
        """
        Format milliseconds into string foramt '00:00:00.000'
        :return: string
        """
        return time.strftime('%H:%M:%S.{}'.format(ms_time % 1000), time.gmtime(ms_time / 1000.0))

    @staticmethod
    def parse_ms(str_time):
        """
        Convert time '00:00:00[(,|.)000]' to integer milliseconds
        :param str_time:
        :return: milliseconds
        """
        "convert from srt time format (0...999) to stl one (0...25)"
        st = re.split('[.,]', str_time)
        tm = st[0].split(':')
        ms = int(st[1]) if len(st) > 1 else 0
        if len(tm) != 3:
            raise ValueError("Expected string format 00:00:00[.000] or 00:00:00[,000]")
        return (int(tm[0]) * 3600 + int(tm[1]) * 60 + int(tm[2])) * 1000 + ms


class SrtUtil(object):
    @staticmethod
    def parse_srt(filename):
        """
        Parse a srt file into a list of objects (number, start, end, content)
        From https://stackoverflow.com/questions/23620423/parsing-a-srt-file-with-regex/23620620
        :param filename:
        :return:
        """
        with open(filename, 'r') as f:
            res = [list(g) for b, g in groupby(f, lambda x: bool(x.strip())) if b]

            # parse
            Subtitle = namedtuple('Subtitle', 'number start end content')
            subs = []
            for sub in res:
                if len(sub) >= 3:  # not strictly necessary, but better safe than sorry
                    sub = [x.strip() for x in sub]
                    number, start_end, content = sub[0], sub[1], sub[2:]  # py 2 syntax
                    start, end = start_end.split(' --> ')
                    subs.append(Subtitle(number, TimeUtil.parse_ms(start), TimeUtil.parse_ms(end), content))
        return subs


class ImageUtil(object):
    @staticmethod
    def vertical_stitch(images, output):
        if images is None or len(images) < 1:
            return False
        ImageFile = namedtuple('ImageFile', 'filename width height')
        width = max(images, key=lambda x: x.width).width
        height = sum(map(lambda x: x.down - x.up, images))
        result = Image.new('RGB', (width, height))
        y_offset = 0
        for image in images:
            img = Image.open(image.image_file)
            cropped = img.crop((0, image.up, image.width, image.down))
            result.paste(cropped, (0, y_offset))
            y_offset += image.down - image.up

        result.save(output)
        return ImageFile(output, width, height)


class TempFileUtil(object):
    @staticmethod
    def get_temp_file(prefix='', suffix=''):
        temp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix)
        temp_file.close()
        return temp_file.name
