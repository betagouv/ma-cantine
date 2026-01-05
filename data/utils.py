import datetime
from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from PIL import ExifTags
from PIL import Image as Img


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def has_charfield_missing_query(field_name):
    return Q(**{f"{field_name}__isnull": True}) | Q(**{f"{field_name}": ""}) | Q(**{f"{field_name}": None})


def has_arrayfield_missing_query(field_name):
    return Q(**{f"{field_name}__isnull": True}) | Q(**{f"{field_name}": []}) | Q(**{f"{field_name}": None})


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


def get_diagnostic_lowest_limit_year():
    return 2019


def get_diagnostic_lower_limit_year():
    return datetime.datetime.now().date().year - 1


def get_diagnostic_upper_limit_year():
    return datetime.datetime.now().date().year + 1


def make_optional_positive_decimal_field(**kwargs):
    return models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal("0"))], **kwargs
    )


def sum_int_with_potential_null(values_to_sum):
    if all(value is None for value in values_to_sum):
        return 0
    else:
        return sum(value for value in values_to_sum if value is not None)
