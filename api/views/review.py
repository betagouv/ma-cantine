import logging
from api.exceptions import DuplicateException
from api.serializers import ReviewSerializer
from data.models import Review, Canteen, Diagnostic
from django.db import IntegrityError
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

logger = logging.getLogger(__name__)


class ReviewView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Review
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        try:
            user = self.request.user
            hasCanteen = Canteen.objects.filter(managers=user).exists()
            hasDiagnostic = Diagnostic.objects.filter(canteen__managers=user).exists()
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, hasCanteen=hasCanteen, hasDiagnostic=hasDiagnostic)
        except IntegrityError as e:
            logger.exception(
                f"User with id {user.id} attempted to create second review for page {serializer.validated_data['page']}:\n{e}"
            )
            raise DuplicateException()
