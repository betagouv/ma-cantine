from django_filters import rest_framework as django_filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView

from api.permissions import IsAuthenticated
from api.serializers import InvitationSerializer
from data.models import Invitation


class InvitationFilterSet(django_filters.FilterSet):
    direction = django_filters.ChoiceFilter(choices=Invitation.Direction.choices)  # annotated

    class Meta:
        model = Invitation
        fields = ["category", "status", "creation_canteen", "invited_canteen", "direction"]


@extend_schema_view(
    get=extend_schema(
        summary="Lister les invitations qui concernent l'utilisateur.",
        description="Invitations envoyées par ou reçues par les cantines gérées par l'utilisateur.",
        tags=["Cantines"],
    ),
)
class UserInvitationsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Invitation.objects.none()  # see get_queryset
    serializer_class = InvitationSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = InvitationFilterSet

    def get_queryset(self):
        user = self.request.user
        return (
            Invitation.objects.for_user(user)
            .annotate_with_direction(user)
            .select_related("creation_canteen", "invited_canteen")
            .order_by("-creation_date")
        )
