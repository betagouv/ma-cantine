from io import BytesIO
from PIL import Image as Img
from PIL import ExifTags
from django.core.files.base import ContentFile


def _needs_rotation(pillow_image):
    orientation_tag = next(filter(lambda x: ExifTags.TAGS[x] == "Orientation", ExifTags.TAGS), None)
    exif_data = pillow_image._getexif()

    return exif_data and orientation_tag


def _rotate_image(pillow_image):
    needs_rotation = _needs_rotation(pillow_image)
    if not needs_rotation:
        return pillow_image

    orientation_tag = next(filter(lambda x: ExifTags.TAGS[x] == "Orientation", ExifTags.TAGS), None)
    exif_data = pillow_image._getexif()
    orientation = dict(exif_data.items()).get(orientation_tag)

    if orientation == 3:
        return pillow_image.rotate(180, expand=True)
    if orientation == 6:
        return pillow_image.rotate(270, expand=True)
    if orientation == 8:
        return pillow_image.rotate(90, expand=True)
    return pillow_image


def _needs_resize(pillow_image, max_size):
    return pillow_image.width > max_size or pillow_image.height > max_size


def _resize_image(pillow_image, max_size):
    needs_resize = _needs_resize(pillow_image, max_size)
    if not needs_resize:
        return pillow_image

    if pillow_image.width >= pillow_image.height:
        new_width = max_size
        new_height = max_size * pillow_image.height / pillow_image.width
    else:
        new_width = max_size * pillow_image.width / pillow_image.height
        new_height = max_size

    return pillow_image.resize((int(new_width), int(new_height)))


def _needs_alpha_channel_removal(pillow_image):
    return pillow_image.mode in ("RGBA", "LA")


def _remove_alpha_channel(pillow_image):
    if _needs_alpha_channel_removal(pillow_image):
        background = Img.new(pillow_image.mode[:-1], pillow_image.size, "#FFFFFF")
        background.paste(pillow_image, pillow_image.split()[-1])
        pillow_image = background
    return pillow_image


def optimize_image(image, name, max_size=1600):
    try:
        image_format = "jpeg"
        pillow_image = Img.open(image)

        if (
            not _needs_resize(pillow_image, max_size)
            and not _needs_rotation(pillow_image)
            and not _needs_alpha_channel_removal(pillow_image)
        ):
            return image

        pillow_image = _rotate_image(pillow_image)
        pillow_image = _resize_image(pillow_image, max_size)
        pillow_image = _remove_alpha_channel(pillow_image)

        output = BytesIO()
        pillow_image.save(output, format=image_format)
        media_content = output.getvalue()

        if media_content:
            return ContentFile(media_content, name=name)
        else:
            return image
    except Exception:
        return image


def get_region(department_code):
    code_department_to_region = {
        "01": "84",
        "02": "32",
        "03": "84",
        "04": "93",
        "05": "93",
        "06": "93",
        "07": "84",
        "08": "44",
        "09": "76",
        "10": "44",
        "11": "76",
        "12": "76",
        "13": "93",
        "14": "28",
        "15": "84",
        "16": "75",
        "17": "75",
        "18": "24",
        "19": "75",
        "21": "27",
        "22": "53",
        "23": "75",
        "24": "75",
        "25": "27",
        "26": "84",
        "27": "28",
        "28": "24",
        "29": "53",
        "2A": "94",
        "2B": "94",
        "30": "76",
        "31": "76",
        "32": "76",
        "33": "75",
        "34": "76",
        "35": "53",
        "36": "24",
        "37": "24",
        "38": "84",
        "39": "27",
        "40": "75",
        "41": "24",
        "42": "84",
        "43": "84",
        "44": "52",
        "45": "24",
        "46": "76",
        "47": "75",
        "48": "76",
        "49": "52",
        "50": "28",
        "51": "44",
        "52": "44",
        "53": "52",
        "54": "44",
        "55": "44",
        "56": "53",
        "57": "44",
        "58": "27",
        "59": "32",
        "60": "32",
        "61": "28",
        "62": "32",
        "63": "84",
        "64": "75",
        "65": "76",
        "66": "76",
        "67": "44",
        "68": "44",
        "69": "84",
        "70": "27",
        "71": "27",
        "72": "52",
        "73": "84",
        "74": "84",
        "75": "11",
        "76": "28",
        "77": "11",
        "78": "11",
        "79": "75",
        "80": "32",
        "81": "76",
        "82": "76",
        "83": "93",
        "84": "93",
        "85": "52",
        "86": "75",
        "87": "75",
        "88": "44",
        "89": "27",
        "90": "27",
        "91": "11",
        "92": "11",
        "93": "11",
        "94": "11",
        "95": "11",
        "971": "01",
        "972": "02",
        "973": "03",
        "974": "04",
        "976": "06",
    }
    if department_code and department_code in code_department_to_region:
        return code_department_to_region[department_code]
