from rest_framework import permissions
from django.contrib.auth import get_user_model
from data.models import Canteen, Diagnostic, Teledeclaration


class IsProfileOwner(permissions.BasePermission):
    """
    This is for actions only permitted if the authenticated
    user is the profile (user model) owner
    """

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, get_user_model()):
            return False
        return request.user and request.user == obj


class IsCanteenManager(permissions.BasePermission):
    """
    This is for actions only permitted by managers of
    a canteen
    """

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Canteen):
            return False
        return obj in request.user.canteens.all()


class CanEditDiagnostic(permissions.BasePermission):
    """
    This is for actions only permitted by managers of
    the diagnostic's canteen
    """

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Diagnostic):
            return False
        is_manager = request.user in obj.canteen.managers.all()
        has_submitted_teledeclaration = (
            obj.teledeclaration_set.filter(
                status=Teledeclaration.TeledeclarationStatus.SUBMITTED
            ).count()
            > 0
        )

        return is_manager and not has_submitted_teledeclaration
