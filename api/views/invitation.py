from django.db.models import Q
from django_filters import rest_framework as django_filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView

from api.permissions import IsAuthenticated
from api.serializers import InvitationSerializer
from data.models import Invitation


class InvitationFilterSet(django_filters.FilterSet):
    class Meta:
        model = Invitation
        fields = ["category", "status", "creation_canteen", "invited_canteen"]


@extend_schema_view(
    get=extend_schema(
        summary="Lister les invitations qui concernent l'utilisateur.",
        description="Invitations envoyées par ou reçues par les cantines gérées par l'utilisateur.",
        tags=["Cantines"],
    ),
)
class UserInvitationsListView(ListAPIView):
    permission_classes = [IsAuthenticated]  # not available via OAuth2 (yet)
    queryset = Invitation.objects.none()  # see get_queryset
    serializer_class = InvitationSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = InvitationFilterSet

    def get_queryset(self):
        user_canteen_ids = self.request.user.canteens.values("id")
        return (
            Invitation.objects.filter(
                Q(creation_canteen_id__in=user_canteen_ids) | Q(invited_canteen_id__in=user_canteen_ids)
            )
            .select_related("creation_canteen", "invited_canteen")
            .order_by("-creation_date")
        )
