from django.test import TestCase

from common.utils.camelize import camelize


class CamelizeTest(TestCase):
    def test_camelize_string(self):
        for TUPLE in [
            ("some_value", "someValue"),
            ("already_camel_ish", "alreadyCamelIsh"),
            ("no_underscores_left_", "noUnderscoresLeft_"),
            ("nounderscore", "nounderscore"),
            ("", ""),
        ]:
            with self.subTest(text=TUPLE):
                self.assertEqual(camelize(TUPLE[0]), TUPLE[1])

    def test_camelize_dict(self):
        self.assertEqual(
            camelize({"some_key": 1, "another_key": {"nested_key": 2}}),
            {"someKey": 1, "anotherKey": {"nestedKey": 2}},
        )

    def test_camelize_list(self):
        self.assertEqual(
            camelize([{"some_key": 1}, {"another_key": 2}]),
            [{"someKey": 1}, {"anotherKey": 2}],
        )

    def test_camelize_empty_dict(self):
        self.assertEqual(camelize({}), {})

    def test_camelize_empty_list(self):
        self.assertEqual(camelize([]), [])
