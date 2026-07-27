import base64
import os

from django.core.files import File
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories.canteen import CanteenFactory
from data.models import CanteenImage

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class CanteenLogoUploadApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_logo", kwargs={"canteen_pk": cls.canteen.pk})

    def test_cannot_upload_canteen_logo_if_unauthenticated(self):
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_upload_canteen_logo_if_canteen_unknown(self):
        url = reverse("canteen_logo", kwargs={"canteen_pk": 999})
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_upload_canteen_logo_if_not_canteen_manager(self):
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_upload_canteen_logo(self):
        self.canteen.managers.add(authenticate.user)
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("logo", body)

    def test_upload_canteen_logo_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("logo", body)

    @authenticate
    def test_upload_canteen_logo_even_if_canteen_not_filled(self):
        self.canteen.managers.add(authenticate.user)
        self.canteen.siret = None
        self.canteen.save(skip_validations=True)
        self.assertIsNone(self.canteen.siret)
        self.assertFalse(self.canteen.is_filled)

        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("logo", body)

    @authenticate
    def test_can_replace_existing_logo(self):
        self.canteen.managers.add(authenticate.user)

        # First upload a logo
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        # Now replace it with a new logo
        new_image_path = os.path.join(CURRENT_DIR, "files/test-image-2.jpg")
        with open(new_image_path, "rb") as new_image:
            new_image_base_64 = base64.b64encode(new_image.read()).decode("utf-8")

        new_payload = {
            "logo": "data:image/jpeg;base64," + new_image_base_64,
        }
        response = self.client.post(self.url, data=new_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("logo", body)


class CanteenLogoRetrieveApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_logo", kwargs={"canteen_pk": cls.canteen.pk})

    def test_cannot_retrieve_canteen_logo_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_retrieve_canteen_logo_if_canteen_unknown(self):
        url = reverse("canteen_logo", kwargs={"canteen_pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_retrieve_canteen_logo_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_retrieve_canteen_logo(self):
        self.canteen.managers.add(authenticate.user)

        # First upload a logo
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        # Now retrieve the logo
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("logo", body)

    def test_retrieve_canteen_logo_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")

        # First upload a logo
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        # Now retrieve the logo
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("logo", body)


class CanteenLogoDeleteApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_logo", kwargs={"canteen_pk": cls.canteen.pk})

    def test_cannot_delete_canteen_logo_if_unauthenticated(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_delete_canteen_logo_if_canteen_unknown(self):
        url = reverse("canteen_logo", kwargs={"canteen_pk": 999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_delete_canteen_logo_if_not_canteen_manager(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_delete_canteen_logo(self):
        self.canteen.managers.add(authenticate.user)

        # First upload a logo
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        # Now delete the logo
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_canteen_logo_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")

        # First upload a logo
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        # Now delete the logo
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @authenticate
    def test_delete_canteen_logo_even_if_canteen_not_filled(self):
        self.canteen.managers.add(authenticate.user)
        self.canteen.siret = None
        self.canteen.save(skip_validations=True)
        self.assertIsNone(self.canteen.siret)
        self.assertFalse(self.canteen.is_filled)

        # First upload a logo
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "logo": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        # Now delete the logo
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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
        cls.url = reverse("canteen_images_list_create", kwargs={"canteen_pk": cls.canteen.pk})

    def test_cannot_get_canteen_images_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_canteen_images_if_canteen_does_not_exist(self):
        url = reverse("canteen_images_list_create", kwargs={"canteen_pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_canteen_images_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_canteen_images(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 3)
        for item in body:
            self.assertIn("id", item)
            self.assertIn("image", item)
            self.assertIn("altText", item)

    def test_get_canteen_images_via_oauth2(self):
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


class CanteenImagesDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        image_name = "test-image-1.jpg"
        path = os.path.join(CURRENT_DIR, f"files/{image_name}")
        with open(path, "rb") as image:
            file = File(image)
            file.name = image_name
            canteen_image = CanteenImage(image=file)
            canteen_image.canteen = cls.canteen
            canteen_image.save()
        cls.url = reverse(
            "canteen_images_retrieve_update_destroy",
            kwargs={"canteen_pk": cls.canteen.pk, "pk": cls.canteen.images.first().pk},
        )

    def test_cannot_get_canteen_image_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_canteen_image_if_canteen_does_not_exist(self):
        url = reverse("canteen_images_retrieve_update_destroy", kwargs={"canteen_pk": 9999, "pk": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_canteen_image_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_canteen_image_detail(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)

    def test_get_canteen_image_detail_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)


class CanteenImagesCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_images_list_create", kwargs={"canteen_pk": cls.canteen.pk})

    def test_cannot_create_canteen_image_if_unauthenticated(self):
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_canteen_image_if_canteen_does_not_exist(self):
        url = reverse("canteen_images_list_create", kwargs={"canteen_pk": 9999})
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_canteen_image_if_not_canteen_manager(self):
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_canteen_image(self):
        self.canteen.managers.add(authenticate.user)
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "image": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)
        self.assertIsNone(body["altText"])

    def test_create_canteen_image_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "image": "data:image/jpeg;base64," + image_base_64,
            "altText": "Test image 1",  # optional field
        }
        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)
        self.assertEqual(body["altText"], "Test image 1")

    @authenticate
    def test_create_canteen_image_even_if_canteen_not_filled(self):
        self.canteen.managers.add(authenticate.user)
        self.canteen.siret = None
        self.canteen.save(skip_validations=True)
        self.assertIsNone(self.canteen.siret)
        self.assertFalse(self.canteen.is_filled)

        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "image": "data:image/jpeg;base64," + image_base_64,
        }
        response = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)


class CanteenImagesUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        image_name = "test-image-1.jpg"
        path = os.path.join(CURRENT_DIR, f"files/{image_name}")
        with open(path, "rb") as image:
            file = File(image)
            file.name = image_name
            canteen_image = CanteenImage(image=file)
            canteen_image.canteen = cls.canteen
            canteen_image.save()
        cls.url = reverse(
            "canteen_images_retrieve_update_destroy",
            kwargs={"canteen_pk": cls.canteen.pk, "pk": cls.canteen.images.first().pk},
        )

    def test_cannot_update_canteen_image_if_unauthenticated(self):
        response = self.client.patch(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_update_canteen_image_if_canteen_does_not_exist(self):
        url = reverse("canteen_images_retrieve_update_destroy", kwargs={"canteen_pk": 9999, "pk": 1})
        response = self.client.patch(url, data={})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_update_canteen_image_if_not_canteen_manager(self):
        response = self.client.patch(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_update_canteen_image(self):
        self.canteen.managers.add(authenticate.user)
        self.assertEqual(self.canteen.images.first().alt_text, None)

        payload = {
            "altText": "Updated alt text",
        }
        response = self.client.patch(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)
        self.assertEqual(body["altText"], "Updated alt text")

    def test_update_canteen_image_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")
        self.assertEqual(self.canteen.images.first().alt_text, None)

        payload = {
            "altText": "Updated alt text via OAuth2",
        }
        response = self.client.patch(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)
        self.assertEqual(body["altText"], "Updated alt text via OAuth2")

    @authenticate
    def test_update_canteen_image_even_if_canteen_not_filled(self):
        self.canteen.managers.add(authenticate.user)
        self.canteen.siret = None
        self.canteen.save(skip_validations=True)
        self.assertIsNone(self.canteen.siret)
        self.assertFalse(self.canteen.is_filled)
        self.assertEqual(self.canteen.images.first().alt_text, None)

        payload = {
            "altText": "Updated alt text even if canteen not filled",
        }
        response = self.client.patch(self.url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("id", body)
        self.assertIn("image", body)
        self.assertIn("altText", body)
        self.assertEqual(body["altText"], "Updated alt text even if canteen not filled")


class CanteenImagesDeleteApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        image_name = "test-image-1.jpg"
        path = os.path.join(CURRENT_DIR, f"files/{image_name}")
        with open(path, "rb") as image:
            file = File(image)
            file.name = image_name
            canteen_image = CanteenImage(image=file)
            canteen_image.canteen = cls.canteen
            canteen_image.save()
        cls.url = reverse(
            "canteen_images_retrieve_update_destroy",
            kwargs={"canteen_pk": cls.canteen.pk, "pk": cls.canteen.images.first().pk},
        )

    def test_cannot_delete_canteen_image_if_unauthenticated(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_delete_canteen_image_if_canteen_does_not_exist(self):
        url = reverse("canteen_images_retrieve_update_destroy", kwargs={"canteen_pk": 9999, "pk": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_delete_canteen_image_if_not_canteen_manager(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_delete_canteen_image_if_image_does_not_exist(self):
        url = reverse("canteen_images_retrieve_update_destroy", kwargs={"canteen_pk": self.canteen.pk, "pk": 9999})
        self.canteen.managers.add(authenticate.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_delete_canteen_image(self):
        self.canteen.managers.add(authenticate.user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_canteen_image_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @authenticate
    def test_delete_canteen_image_even_if_canteen_not_filled(self):
        self.canteen.managers.add(authenticate.user)
        self.canteen.siret = None
        self.canteen.save(skip_validations=True)
        self.assertIsNone(self.canteen.siret)
        self.assertFalse(self.canteen.is_filled)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
