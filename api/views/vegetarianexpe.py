from django.http import HttpResponse
from api.permissions import IsLinkedCanteenManager, IsAuthenticated
from api.serializers import VegetarianExpeSerializer
from api.exceptions import DuplicateException
from data.models import VegetarianExpe, Canteen
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
import logging
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin

logger = logging.getLogger(__name__)


class VegetarianExpeView(CreateModelMixin, RetrieveUpdateAPIView):
    model = VegetarianExpe
    serializer_class = VegetarianExpeSerializer
    queryset = VegetarianExpe.objects.all()
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            "canteen": self.kwargs["canteen_pk"],
        }
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return HttpResponse(status=204)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        canteen_id = self.request.parser_context.get("kwargs").get("canteen_pk")
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            if not canteen.managers.filter(pk=self.request.user.pk).exists():
                logger.error(
                    f"User {self.request.user.id} attempted to create a vegetarian expe in someone else's canteen: {canteen_id}"
                )
                raise PermissionDenied()
            if self.get_queryset().filter(canteen=canteen).exists():
                logger.error(
                    f"User {self.request.user.id} attempted to create a duplicate vegetarian expe in canteen {canteen_id}"
                )
                raise DuplicateException("Canteen already has a vegetarian expe")
            serializer.is_valid(raise_exception=True)
            serializer.save(canteen=canteen)
        except ObjectDoesNotExist as e:
            logger.error(
                f"User {self.request.user.id} attempted to create a vegetarian expe in nonexistent canteen {canteen_id}"
            )
            raise NotFound() from e

    def post(self, request, *args, **kwargs):
        return self.create(request)
