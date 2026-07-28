from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.http import JsonResponse
from rest_framework import status

from api.permissions import IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam
from data.models import CanteenImage, Canteen
from api.serializers.canteen_images import CanteenImageSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Lister les images d'une cantine.",
        description="",
        tags=["Cantines"],
        responses=CanteenImageSerializer(many=True),
    ),
    post=extend_schema(
        summary="Ajouter une image.",
        description="",
        tags=["Cantines"],
    ),
)
class UserCanteenImagesListView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    model = CanteenImage
    serializer_class = CanteenImageSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return canteen.images.all()

    def perform_create(self, serializer):
        canteen = self._get_canteen()
        serializer.save(canteen=canteen)


@extend_schema_view(
    delete=extend_schema(
        summary="Supprimer une image.",
        description="",
        tags=["Cantines"],
    ),
)
class UserCanteenImagesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    model = CanteenImage
    serializer_class = CanteenImageSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return canteen.images.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Only PATCH request supported in this resource"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
