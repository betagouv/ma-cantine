from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response

from api.permissions import IsCanteenManager
from api.serializers import ResourceActionSerializer
from data.models import Canteen, ResourceAction, WasteAction


class ResourceActionView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = ResourceAction
    queryset = ResourceAction.objects.all()
    serializer_class = ResourceActionSerializer

    def create(self, request, *args, **kwargs):
        # get resource
        self.resource = get_object_or_404(WasteAction, pk=kwargs.get("resource_pk"))
        # get canteen and check permissions
        canteen_id = request.data.get("canteen_id")
        try:
            self.canteen = Canteen.objects.get(pk=canteen_id)
        except Canteen.DoesNotExist:
            raise ValidationError({"canteen_id": "La cantine spécifiée n'existe pas"})
        if not IsCanteenManager().has_object_permission(request, self, self.canteen):
            raise PermissionDenied()
        # update or create resource action
        try:
            resource_action = ResourceAction.objects.get(resource=self.resource, canteen=self.canteen)
            serializer = self.get_serializer(resource_action)
            serializer.update(resource_action, request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ResourceAction.DoesNotExist:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(resource=self.resource)
