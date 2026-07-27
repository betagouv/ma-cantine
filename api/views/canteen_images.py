from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view

from api.permissions import IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam
from data.models import CanteenImage, Canteen

from api.serializers.canteen_images import CanteenImageSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Lister les images d'une cantine.",
        description="",
        tags=["Cantines"],
        responses=CanteenImageSerializer(many=True),
    )
)
class UserCanteenImagesListView(ListAPIView):
    model = CanteenImage
    serializer_class = CanteenImageSerializer
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return canteen.images.all()
