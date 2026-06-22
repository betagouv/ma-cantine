from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, PurchaseFactory


class PurchaseFactureUploadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.purchase = PurchaseFactory(canteen=cls.canteen)
        cls.url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": cls.canteen.id, "pk": cls.purchase.id},
        )

    def test_cannot_upload_if_unauthenticated(self):
        file = SimpleUploadedFile("facture.pdf", b"pdf content")
        response = self.client.post(self.url, {"facture": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_upload_if_canteen_unknown(self):
        url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": 9999, "pk": self.purchase.id},
        )
        file = SimpleUploadedFile("facture.pdf", b"pdf content")
        response = self.client.post(url, {"facture": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_upload_if_not_canteen_manager(self):
        file = SimpleUploadedFile("facture.pdf", b"pdf content")
        response = self.client.post(self.url, {"facture": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_upload_if_purchase_unknown(self):
        self.canteen.managers.add(authenticate.user)
        url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": self.canteen.id, "pk": 9999},
        )
        file = SimpleUploadedFile("facture.pdf", b"pdf content")

        response = self.client.post(url, {"facture": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_upload_if_file_missing(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.post(self.url, {}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_upload_if_purchase_not_in_corresponding_canteen(self):
        canteen_other = CanteenFactory()
        purchase_other = PurchaseFactory(canteen=canteen_other)
        url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": self.canteen.id, "pk": purchase_other.id},
        )
        self.canteen.managers.add(authenticate.user)
        file = SimpleUploadedFile("facture.pdf", b"pdf content")

        response = self.client.post(url, {"facture": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_can_upload_facture(self):
        self.canteen.managers.add(authenticate.user)
        file = SimpleUploadedFile("facture.pdf", b"pdf content")

        response = self.client.post(self.url, {"facture": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], self.purchase.id)
        self.assertIsNotNone(data["facture"])

        # Verify file was saved
        self.purchase.refresh_from_db()
        self.assertTrue(self.purchase.facture)
        self.assertIn("facture", self.purchase.facture.name)

    @authenticate
    def test_can_replace_existing_facture(self):
        self.canteen.managers.add(authenticate.user)
        old_file = SimpleUploadedFile("old.pdf", b"old content")
        self.purchase.facture = old_file
        self.purchase.save()
        old_file_name = self.purchase.facture.name

        new_file = SimpleUploadedFile("new.pdf", b"new content")
        response = self.client.post(self.url, {"facture": new_file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase.refresh_from_db()
        self.assertNotEqual(self.purchase.facture.name, old_file_name)


class PurchaseFactureDeleteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.purchase = PurchaseFactory(canteen=cls.canteen)
        cls.url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": cls.canteen.id, "pk": cls.purchase.id},
        )

    def test_cannot_delete_if_unauthenticated(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_delete_if_canteen_unknown(self):
        url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": 9999, "pk": self.purchase.id},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_delete_if_not_canteen_manager(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_delete_if_purchase_unknown(self):
        self.canteen.managers.add(authenticate.user)
        url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": self.canteen.id, "pk": 9999},
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_delete_if_purchase_not_in_corresponding_canteen(self):
        canteen_other = CanteenFactory()
        purchase_other = PurchaseFactory(canteen=canteen_other)
        url = reverse(
            "purchase_facture",
            kwargs={"canteen_pk": self.canteen.id, "pk": purchase_other.id},
        )
        self.canteen.managers.add(authenticate.user)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_can_delete_facture(self):
        self.canteen.managers.add(authenticate.user)
        file = SimpleUploadedFile("facture.pdf", b"pdf content")
        self.purchase.facture = file
        self.purchase.save()
        self.assertTrue(self.purchase.facture)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.purchase.refresh_from_db()
        self.assertFalse(self.purchase.facture)

    @authenticate
    def test_can_delete_even_if_purchase_has_no_facture(self):
        self.canteen.managers.add(authenticate.user)
        self.assertFalse(self.purchase.facture)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.purchase.refresh_from_db()
        self.assertFalse(self.purchase.facture)
