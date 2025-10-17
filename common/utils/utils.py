def normalize_string(text: str) -> str:
    if text:
        return text.replace(" ", "").replace("\xa0", "")
    return text


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
