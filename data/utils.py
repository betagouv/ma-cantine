from io import BytesIO
from PIL import Image as Img
from PIL import ExifTags
from django.core.files.base import ContentFile


def _needs_rotation(pillow_image):
    orientation_tag = next(
        filter(lambda x: ExifTags.TAGS[x] == "Orientation", ExifTags.TAGS), None
    )
    exif_data = pillow_image._getexif()

    return exif_data and orientation_tag


def _rotate_image(pillow_image):
    needs_rotation = _needs_rotation(pillow_image)
    if not needs_rotation:
        return pillow_image

    orientation_tag = next(
        filter(lambda x: ExifTags.TAGS[x] == "Orientation", ExifTags.TAGS), None
    )
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

