from rest_framework.test import APITestCase

from api.serializers.utils import safe_to_float


class TestUtils(APITestCase):

    def test_safe_to_float(self):
        test_cases = [
            (None, None),
            ("", None),
            ("abc", None),
            ("123", 123.0),
            (123, 123.0),
            (123.45, 123.45),
            ([], None),
            ({}, None),
            (True, 1.0),
            (False, 0.0),
            ("  42.5  ", 42.5),
        ]
        for input_value, expected in test_cases:
            result = safe_to_float(input_value)
            self.assertEqual(result, expected, msg=f"Failed for input: {input_value!r}")
