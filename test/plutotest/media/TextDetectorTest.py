import os
import cv2

from plutotest.TempFileTestCase import TempFileTestCase
from pluto.media.TextDetector import TextDetector, Rect


class TextDetectorTest(TempFileTestCase):

    def setUp(self):
        super(TextDetectorTest, self).setUp()
        self.text_detector = TextDetector()

    def test_detect_text_rect(self):
        # image = cv2.imread(os.path.join(self.base_dir, 'images', '1.jpg'))
        image = cv2.imread(os.path.join(self.base_dir, 'clips', 'tang.mp4_1731.jpg'))

        rectangles = self.text_detector.detect_text_rect(image)
        # self.assertEqual(1, len(rectangles))
        # self.assertEqual(Rect([87, 268, 465, 47]), rectangles[0])
        # Manual test
        for rect in rectangles:
            cv2.rectangle(image, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), (255, 0, 255), 2)
        # temp_file = self.get_temp_file()
        cv2.imwrite(self.get_temp_file(delete=False), image)
        # actual = cv2.imread(temp_file)
        # Manual test
        # cv2.imshow('captcha_result', image)
        # cv2.waitKey()

    def test_text_subtitle(self):
        up, down = self.text_detector.detect_subtitle_range(os.path.join(self.base_dir, 'images', '1.jpg'))
        self.assertEqual((270, 360), (up, down))
