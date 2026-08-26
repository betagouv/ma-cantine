import logging

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, tokens
from django.contrib.auth import views as auth_views
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import FormView, TemplateView, View

from common.utils import send_mail
from web.forms import LoginUserForm, RegisterUserForm

logger = logging.getLogger(__name__)

if settings.USES_MONCOMPTEPRO:
    oauth = OAuth()
    oauth.register(
        name="moncomptepro",
        server_metadata_url=settings.MONCOMPTEPRO_CONFIG,
        client_kwargs={"scope": "openid email profile organizations"},
    )


class WidgetView(TemplateView):
    template_name = "vue-app.html"

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_widget"] = True
        return context


class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue-app.html"


class Vue3AppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue3-app.html"


class LoginUserView(auth_views.LoginView):
    form_class = LoginUserForm

    def form_invalid(self, form):
        # Check if error is due to unconfirmed email
        error_msg = str(form.errors)
        if "email n'a pas encore été confirmée" in error_msg:
            username = form.cleaned_data.get("username", "")

            try:
                # Send activation email without logging in
                _send_activation_email(username, self.request)

                # Add message and redirect to registration_done page with username
                messages.info(
                    self.request,
                    "Votre adresse email n'a pas été confirmée. Un nouvel email de confirmation a été envoyé.",
                )
                return redirect("registration_email_sent", username=username, from_registration=False)
            except Exception:
                # If email sending fails, fall through to default handling
                pass

        return super().form_invalid(form)


class RegisterUserView(FormView):
    """
    View containing the user-only form to create an account
    """

    form_class = RegisterUserForm
    template_name = "auth/register.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["email"] = self.request.GET.get("email") if self.request.GET else None
        return initial

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        try:
            # Send activation email (redirects to registration_done page with username)
            return redirect("registration_email_sent", username=username, from_registration=True)
        except Exception:
            self.success_url = reverse_lazy("registration_email_sent_error", kwargs={"username": username})
            return super().form_valid(form)


class ActivationTokenView(View):
    """
    View allowing to resend an activation email
    """

    def get(self, request, *args, **kwargs):
        return render(request, "auth/register_resend_email.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        try:
            # Send activation email
            _send_activation_email(username, self.request)
            return redirect(reverse_lazy("registration_done"))
        except Exception:
            return redirect(reverse_lazy("registration_email_sent_error", kwargs={"username": username}))


class RegisterDoneView(TemplateView):
    """
    This view is used after the registration form
    to indicate a confirmation email has been sent
    """

    template_name = "auth/register_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = kwargs.get("username", "")
        context["from_registration"] = kwargs.get("from_registration", False)
        return context


class RegisterSendMailFailedView(TemplateView):
    """
    This view is used when an error occurred when sending mail
    """

    template_name = "auth/register_send_mail_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        has_canteens = not self.request.user.is_anonymous and self.request.user.canteens.count() > 0
        context["redirection_url"] = reverse_lazy("app") if has_canteens else "/nouvelle-cantine"
        return context


class RegisterInvalidTokenView(TemplateView):
    """
    This view is used after the user clicks in a token
    contained in the registration confirmation email
    but the token is wrong
    """

    template_name = "auth/register_token_invalid.html"


class AccountActivationView(View):
    """
    This view will activate the account of a newly
    registered user
    """

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64", "")
        token = kwargs.get("token", "")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None
        if user and user.email_confirmed:
            messages.info(
                request,
                "Votre adresse email a bien été validée, vous pouvez vous identifier.",
            )
            return redirect(reverse_lazy("login"))
        if user is not None and tokens.default_token_generator.check_token(user, token):
            user.email_confirmed = True
            user.save()
            login(request, user)
            return redirect(reverse_lazy("app"))
        else:
            return redirect(reverse_lazy("invalid_token"))


def _send_activation_email(username, request):
    """
    Send activation email to a user with unconfirmed email.

    Args:
        username: Username or email of the user
        request: Django request object

    Returns:
        HttpResponseRedirect: Redirect to registration_done page

    Raises:
        Exception: If email cannot be sent or user not found
    """
    if not username:
        return redirect(reverse_lazy("app"))

    try:
        # Support both username and email lookup
        user = get_user_model().objects.get(Q(username=username) | Q(email=username), email_confirmed=False)

        # Generate and send activation email
        token = tokens.default_token_generator.make_token(user)
        context = {
            "token": token,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "protocol": settings.PROTOCOL,
            "domain": settings.HOSTNAME,
        }
        send_mail(
            subject="Confirmation de votre adresse email - ma cantine",
            template="auth/account_activate_email",
            context=context,
            to=[user.email],
        )

        # Always redirect to registration_done page
        return redirect(reverse_lazy("registration_done"))

    except get_user_model().DoesNotExist:
        raise Exception("User not found or already confirmed.")
    except Exception as e:
        raise Exception(f"Error occurred: {str(e)}")


class OIDCLoginView(View):
    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri(reverse_lazy("oidc-authorize"))
        return oauth.moncomptepro.authorize_redirect(request, redirect_uri)


class OIDCAuthorizeView(View):
    def get(self, request, *args, **kwargs):
        try:
            token = oauth.moncomptepro.authorize_access_token(request)
            mcp_data = oauth.moncomptepro.userinfo(token=token)
            user = OIDCAuthorizeView.get_or_create_user(mcp_data)
            login(request, user)
            return redirect(reverse_lazy("app"))
        except Exception as e:
            logger.exception("Error authenticating with MonComptePro")
            logger.exception(e)
            return redirect("app")

    @staticmethod
    def get_or_create_user(mcp_data):
        mcp_id = mcp_data.get("sub")
        mcp_email = mcp_data.get("email")

        # Attempt with mcp_id
        try:
            user = get_user_model().objects.get(mcp_id=mcp_id)
            user.mcp_organizations = mcp_data.get("organizations")
            user.save()
            logger.info(f"MonComptePro user {mcp_id} (ID Ma Cantine: {user.id}) was found.")
            return user
        except get_user_model().DoesNotExist:
            pass

        # Attempt with email
        try:
            user = get_user_model().objects.get(email=mcp_email)
            user.mcp_id = mcp_data.get("sub")
            user.mcp_organizations = mcp_data.get("organizations")
            user.save()
            logger.info(f"MonComptePro user {mcp_id} was already registered in MaCantine with email {mcp_email}.")
            return user
        except get_user_model().DoesNotExist:
            pass

        # Create user
        logger.info(f"Creating new user from MonComptePro user {mcp_id} with email {mcp_email}.")
        user = get_user_model().objects.create(
            first_name=mcp_data.get("given_name"),
            last_name=mcp_data.get("family_name"),
            email=mcp_email,
            mcp_id=mcp_id,
            phone_number=mcp_data.get("phone_number"),
            username=f"{mcp_data.get('family_name')}-mcp-{mcp_id}",
            mcp_organizations=mcp_data.get("organizations"),
            created_with_mcp=True,
        )
        return user
