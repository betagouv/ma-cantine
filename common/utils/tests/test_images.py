from io import BytesIO

from django.core.files.base import ContentFile
from django.test import SimpleTestCase
from PIL import Image

from common.utils.images import optimize_image

ORIENTATION_TAG = 0x0112


def _build_image_file(size=(100, 100), mode="RGB", color="red", exif_orientation=None, image_format="JPEG"):
    image = Image.new(mode, size, color)
    save_kwargs = {}
    if exif_orientation is not None:
        exif = image.getexif()
        exif[ORIENTATION_TAG] = exif_orientation
        save_kwargs["exif"] = exif

    buffer = BytesIO()
    image.save(buffer, format=image_format, **save_kwargs)
    buffer.seek(0)
    return buffer


class OptimizeImageTest(SimpleTestCase):
    def test_returns_original_when_no_changes_needed(self):
        image = _build_image_file(size=(100, 100))
        result = optimize_image(image, "test.jpg", max_size=1600)
        self.assertIs(result, image)

    def test_resizes_image_larger_than_max_size(self):
        image = _build_image_file(size=(2000, 1000))
        result = optimize_image(image, "test.jpg", max_size=1600)
        self.assertIsInstance(result, ContentFile)
        resized = Image.open(result)
        self.assertEqual(resized.size, (1600, 800))

    def test_resizes_taller_than_wide_image_preserving_ratio(self):
        image = _build_image_file(size=(1000, 2000))
        result = optimize_image(image, "test.jpg", max_size=1600)
        resized = Image.open(result)
        self.assertEqual(resized.size, (800, 1600))

    def test_removes_alpha_channel(self):
        image = _build_image_file(size=(100, 100), mode="RGBA", color=(255, 0, 0, 128), image_format="PNG")
        result = optimize_image(image, "test.png", max_size=1600)
        self.assertIsInstance(result, ContentFile)
        cleaned = Image.open(result)
        self.assertEqual(cleaned.mode, "RGB")

    def test_rotates_image_based_on_exif_orientation(self):
        image = _build_image_file(size=(200, 100), exif_orientation=6)
        result = optimize_image(image, "test.jpg", max_size=1600)
        self.assertIsInstance(result, ContentFile)
        rotated = Image.open(result)
        self.assertEqual(rotated.size, (100, 200))

    def test_returns_original_on_invalid_image(self):
        invalid = BytesIO(b"not an image")
        result = optimize_image(invalid, "test.jpg", max_size=1600)
        self.assertIs(result, invalid)
