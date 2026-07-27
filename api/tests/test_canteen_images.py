from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import os
from django.core.files import File
from api.tests.utils import authenticate, get_oauth2_token
from data.factories.canteen import CanteenFactory
from data.models import CanteenImage

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class CanteenImagesListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        image_names = [
            "test-image-1.jpg",
            "test-image-2.jpg",
            "test-image-3.png",
        ]
        for image_name in image_names:
            path = os.path.join(CURRENT_DIR, f"files/{image_name}")
            with open(path, "rb") as image:
                file = File(image)
                file.name = image_name
                canteen_image = CanteenImage(image=file)
                canteen_image.canteen = cls.canteen
                canteen_image.save()
        cls.url = reverse("canteen_images_list", kwargs={"canteen_pk": cls.canteen.pk})

    def test_cannot_get_canteen_images_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_canteen_images_if_canteen_does_not_exist(self):
        url = reverse("canteen_images_list", kwargs={"canteen_pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_canteen_images_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_canteen_images_list(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 3)
        for item in body:
            self.assertIn("id", item)
            self.assertIn("image", item)
            self.assertIn("altText", item)

    def test_canteen_images_list_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 3)
        for item in body:
            self.assertIn("id", item)
            self.assertIn("image", item)
            self.assertIn("altText", item)
