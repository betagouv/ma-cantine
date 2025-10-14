def normalize_string(text: str) -> str:
    if text:
        return text.replace(" ", "").replace("\xa0", "")
    return text
