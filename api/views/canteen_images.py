from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam
from api.serializers.canteen_images import CanteenImageSerializer, CanteenLogoSerializer
from data.models import Canteen, CanteenImage


@extend_schema_view(
    get=extend_schema(
        summary="Obtenir le logo d'une cantine.",
        description="",
        tags=["Cantines"],
    ),
    post=extend_schema(
        summary="Ajouter le logo d'une cantine.",
        description="",
        tags=["Cantines"],
    ),
    delete=extend_schema(
        summary="Supprimer le logo d'une cantine.",
        description="",
        tags=["Cantines"],
    ),
)
class UserCanteenLogoView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    http_method_names = ["get", "post", "delete"]

    def _get_canteen(self):
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get(self, request, *args, **kwargs):
        canteen = self._get_canteen()

        if not canteen.logo:
            raise NotFound()

        serializer = CanteenLogoSerializer(canteen, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        canteen = self._get_canteen()

        serializer = CanteenLogoSerializer(canteen, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        canteen.logo = serializer.validated_data["logo"]
        canteen.save(skip_validations=True)

        response_serializer = CanteenLogoSerializer(canteen, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        canteen = self._get_canteen()

        if not canteen.logo:
            raise NotFound()

        canteen.logo.delete(save=False)
        canteen.logo = None
        canteen.save(skip_validations=True)

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les images d'une cantine.",
        description="",
        tags=["Cantines"],
        responses=CanteenImageSerializer(many=True),
    ),
    post=extend_schema(
        summary="Ajouter une image d'une cantine.",
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
        return canteen.images.all().order_by("id")

    def perform_create(self, serializer):
        canteen = self._get_canteen()
        serializer.save(canteen=canteen)


@extend_schema_view(
    delete=extend_schema(
        summary="Supprimer une image d'une cantine.",
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
