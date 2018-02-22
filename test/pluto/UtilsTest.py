import unittest

from pluto.utils import SizeUtil, TimeUtil, SrtUtil


class SizeUtilTest(unittest.TestCase):
    def test_fit(self):
        new_size = SizeUtil.fit(1920, 1080, 600, 400)
        self.assertEqual(600, new_size.width)
        self.assertEqual(337.5, new_size.height)


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
    def testMatch(self):
        subs = SrtUtil.parse_srt("test.srt")
        self.assertEqual(3, len(subs))
        self.assertEqual('the transcript for the whole video is unleashed.', subs[1].content[0])


if __name__ == '__main__':
    unittest.main()
