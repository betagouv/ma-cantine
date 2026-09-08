import unicodedata
import re


def normalize_string(text) -> str:
    if text:
        return str(text).replace(" ", "").replace("\xa0", "")
    return text


def clean_unicode_string(value):
    """
    Clean up problematic Unicode/control characters, including Windows-1252 smart quotes and invisible bytes.
    """
    if not isinstance(value, str):
        return value

    # Replace <U+XXXX> patterns
    def replace_unicode_escape(match):
        hex_code = match.group(1)
        try:
            return chr(int(hex_code, 16))
        except Exception:
            return ""

    value = re.sub(r"<U\+([0-9A-Fa-f]{4})>", replace_unicode_escape, value)

    # Replace Windows-1252 smart quotes and similar
    value = value.replace("", "'").replace("", "'").replace("", '"').replace("", '"')

    # Remove other control characters except \n, \t
    value = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]", "", value)

    # Normalize accents, etc.
    value = unicodedata.normalize("NFC", value)
    return value


def add_validation_error(dict, key, value):
    """
    Build a dictionary of validation errors
    {"field1": ["error1", "error2"], "field2": ["error1"]}
    """
    if key not in dict:
        dict[key] = value
    else:
        if type(dict[key]) is list:
            dict[key] += [value]
        if type(dict[key]) is str:
            dict[key] = [dict[key], value]
    return dict


def merge_validation_errors(dict1, *args):
    """
    Merge multiple validation error dictionaries
    """
    for dict2 in args:
        for key, value in dict2.items():
            dict1 = add_validation_error(dict1, key, value)
    return dict1
