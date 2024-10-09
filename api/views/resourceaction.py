from django.core.exceptions import ValidationError
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, get_object_or_404

from api.permissions import IsCanteenManager
from api.serializers import ResourceActionSerializer
from data.models import Canteen, ResourceAction, WasteAction


class ResourceActionView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = ResourceAction
    queryset = ResourceAction.objects.all()
    serializer_class = ResourceActionSerializer

    def perform_create(self, serializer):
        resource = get_object_or_404(WasteAction, pk=self.request.parser_context.get("kwargs").get("resource_pk"))
        canteen_id = self.request.data.get("canteen_id")
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
        except Canteen.DoesNotExist:
            raise ValidationError({"canteen_id": "La cantine spécifiée n'existe pas"})
        if not IsCanteenManager().has_object_permission(self.request, self, canteen):
            raise PermissionDenied()
        serializer.save(resource=resource, canteen=canteen)
