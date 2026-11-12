from django.test import SimpleTestCase

from common.utils import siret as utils_siret


class SiretUtilsTest(SimpleTestCase):
    def test_normalize_siret(self):
        for TUPLE in [
            # string (CSV, Excel text cell): the spaces are removed
            ("21340172201787", "21340172201787"),
            (" 213 401 722 01787 ", "21340172201787"),
            ("213\xa0401\xa0722\xa001787", "21340172201787"),
            ("05980406200087", "05980406200087"),
            ("", ""),
            (None, None),
            # number (Excel number cell): the leading 0s are added back
            (21340172201787, "21340172201787"),
            (5980406200087, "05980406200087"),
            (5980406200087.0, "05980406200087"),
        ]:
            with self.subTest(siret=TUPLE[0]):
                self.assertEqual(utils_siret.normalize_siret(TUPLE[0]), TUPLE[1])
