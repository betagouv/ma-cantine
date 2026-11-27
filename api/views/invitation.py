from django_filters import rest_framework as django_filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from api.permissions import IsAuthenticated
from api.serializers import InvitationCreateSerializer, InvitationSerializer
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
    post=extend_schema(
        summary="Créer une invitation.",
        description="Uniquement par un gestionnaire de la cantine qui envoie l'invitation.",
        tags=["Cantines"],
    ),
)
class UserInvitationsView(ListCreateAPIView):
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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return InvitationCreateSerializer
        return InvitationSerializer

    def perform_create(self, serializer):
        creation_canteen = serializer.validated_data["creation_canteen"]
        if not creation_canteen.managers.filter(id=self.request.user.id).exists():
            raise PermissionDenied()
        # if ValidationError, it will be raised (and handled by custom_exception_handler)
        serializer.save(creation_user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # return the full representation (with the annotated direction)
        invitation = self.get_queryset().get(id=serializer.instance.id)
        return Response(InvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)
