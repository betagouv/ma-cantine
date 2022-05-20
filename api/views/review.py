import logging
from api.exceptions import DuplicateException
from api.serializers import ReviewSerializer
from data.models import Review, Canteen, Diagnostic
from django.db import IntegrityError
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404

logger = logging.getLogger(__name__)


# TODO: consider returning a list of reviews for better extensibility in the future?
class ReviewView(CreateAPIView, RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Review
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {
            "user": self.request.user,
            "page": self.kwargs["page_pk"],
        }
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        try:
            user = self.request.user
            hasCanteen = Canteen.objects.filter(managers=user).exists()
            hasDiagnostic = Diagnostic.objects.filter(canteen__managers=user).exists()
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, hasCanteen=hasCanteen, hasDiagnostic=hasDiagnostic)
        except IntegrityError:
            logger.error(
                f"User with id {user.id} attempted to create second review for page {serializer.validated_data['page']}"
            )
            raise DuplicateException()
