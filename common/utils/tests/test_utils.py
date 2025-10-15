from django.test import TestCase

from common.utils import utils as utils_utils


class UtilsTest(TestCase):
    def test_normalize_string(self):
        for TUPLE in [
            (" 123 456 789 01234 ", "12345678901234"),
            ("215 903 501 00017", "21590350100017"),
            ("  215 90350100017  ", "21590350100017"),
            ("21590350100017", "21590350100017"),
            ("   ", ""),
            ("", ""),
            (None, None),
        ]:
            with self.subTest(text=TUPLE):
                self.assertEqual(utils_utils.normalize_string(TUPLE[0]), TUPLE[1])
