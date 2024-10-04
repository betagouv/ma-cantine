from django.contrib.auth import get_user_model
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework.permissions import TokenHasResourceScope
from rest_framework import permissions

from data.models import Canteen, Diagnostic, Teledeclaration


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Verifies that the user is authenticated without OAuth
    """

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and not isinstance(request.successful_authenticator, OAuth2Authentication)


class IsAuthenticatedOrTokenHasResourceScope(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = permissions.IsAuthenticated().has_permission(request, view)

        oauth2authenticated = False
        if is_authenticated:
            oauth2authenticated = isinstance(request.successful_authenticator, OAuth2Authentication)

        token_has_scope = TokenHasResourceScope()
        has_web_authentication = is_authenticated and not oauth2authenticated
        return has_web_authentication or token_has_scope.has_permission(request, view)


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
        return obj.managers.filter(id=request.user.id).exists()


class IsElectedOfficial(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_elected_official


class IsCanteenManagerUrlParam(permissions.BasePermission):
    """
    Looks for the url_param `canteen_pk` and checks the user is
    manager of the cantine
    """

    def has_permission(self, request, view):
        canteen_pk = view.kwargs.get("canteen_pk", None)
        if not canteen_pk:
            return False
        try:
            canteen = Canteen.objects.only("managers").get(pk=canteen_pk)
            return canteen.managers.filter(id=request.user.id).exists()
        except Canteen.DoesNotExist:
            return False


class CanEditDiagnostic(permissions.BasePermission):
    """
    This is for actions only permitted by managers of
    the diagnostic's canteen
    """

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Diagnostic):
            return False
        is_manager = obj.canteen.managers.filter(id=request.user.id).exists()
        has_submitted_teledeclaration = (
            obj.teledeclaration_set.filter(status=Teledeclaration.TeledeclarationStatus.SUBMITTED).count() > 0
        )

        return is_manager and not has_submitted_teledeclaration


class IsLinkedCanteenManager(permissions.BasePermission):
    """
    This is for actions only permitted by managers of
    the canteen linked to this object
    """

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, "canteen"):
            return False
        return obj.canteen.managers.filter(id=request.user.id).exists()
