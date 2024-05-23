from rest_framework.test import APITestCase
from api.serializers import MinimalCanteenSerializer
from data.factories import CanteenFactory
from data.models import Canteen


class TestCanteenSerializer(APITestCase):
    def test_get_publication_status_from_model(self):
        canteen = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED)
        serialized_canteen = MinimalCanteenSerializer(canteen).data
        self.assertEqual(serialized_canteen["publication_status"], "published")
