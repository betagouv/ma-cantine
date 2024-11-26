import logging

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, tokens
from django.contrib.auth import views as auth_views
from django.core.exceptions import ObjectDoesNotExist
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

if settings.USES_PROCONNECT:
    oauth = OAuth()
    oauth.register(
        name="proconnect",
        server_metadata_url=settings.PROCONNECT_CONFIG,
        client_kwargs={"scope": "openid email given_name usual_name siret", "leeway": 30},
    )


class WidgetView(TemplateView):
    template_name = "vue-app.html"

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        return super(WidgetView, self).get(request, *args, **kwargs)

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
        return super(RegisterUserView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        try:
            _login_and_send_activation_email(username, self.request)
        except Exception:
            self.success_url = reverse_lazy("registration_email_sent_error", kwargs={"username": username})
            return super().form_valid(form)
        else:
            if self.request.GET.get("next"):
                self.success_url = self.request.GET.get("next")
            elif self.request.user.is_dev:
                self.success_url = "/developpement-et-apis"
            else:
                has_canteens = not self.request.user.is_anonymous and self.request.user.canteens.count() > 0
                self.success_url = reverse_lazy("app") if has_canteens else "/nouvelle-cantine"
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
            return _login_and_send_activation_email(username, self.request)
        except Exception:
            return redirect(reverse_lazy("registration_email_sent_error", kwargs={"username": username}))


class RegisterDoneView(TemplateView):
    """
    This view is used after the registration form
    to indicate a confirmation email has been sent
    """

    template_name = "auth/register_done.html"


class RegisterSendMailFailedView(TemplateView):
    """
    This view is used when an error occured when
    sending mail
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
                "Votre adresse email a bien été validé, vous pouvez vous identifier.",
            )
            return redirect(reverse_lazy("login"))
        if user is not None and tokens.default_token_generator.check_token(user, token):
            user.email_confirmed = True
            user.save()
            login(request, user)
            return redirect(reverse_lazy("app"))
        else:
            return redirect(reverse_lazy("invalid_token"))


def _login_and_send_activation_email(username, request):
    if not username:
        return redirect(reverse_lazy("app"))
    try:
        user = get_user_model().objects.get(username=username, email_confirmed=False)
        login(request, user)

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
        return redirect(reverse_lazy("app"))
    except Exception:
        raise Exception("Error occurred : the mail could not be sent.")


class OIDCLoginView(View):
    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri(reverse_lazy("oidc-authorize"))
        return oauth.proconnect.authorize_redirect(request, redirect_uri)


ID_TOKEN_KEY = "id_token"


class OIDCAuthorizeView(View):
    def get(self, request, *args, **kwargs):
        try:
            token = oauth.proconnect.authorize_access_token(request)
            user_data = OIDCAuthorizeView.userinfo(token)
            user = OIDCAuthorizeView.get_or_create_user(user_data)
            login(request, user)
            return redirect(reverse_lazy("app"))
        except Exception as e:
            logger.exception("Error authenticating with ProConnect")
            logger.exception(e)
            return redirect("app")

    @staticmethod
    def get_or_create_user(user_data):
        user_id = user_data.get("sub")
        email = user_data.get("email")
        siret = user_data.get("siret")
        organizations = [{"siret": siret, "id": siret}]  # recreate old MonComptePro structure

        # Attempt with id provided by Identity Provider
        try:
            user = get_user_model().objects.get(proconnect_id=user_id)
            user.proconnect_organizations = organizations
            user.save()
            logger.info(f"ProConnect user {user_id} (ID Ma Cantine: {user.id}) was found.")
            return user
        except get_user_model().DoesNotExist:
            pass

        # Attempt with email
        try:
            user = get_user_model().objects.get(email=email)
            user.proconnect_id = user_id
            user.proconnect_organizations = organizations
            user.save()
            logger.info(f"ProConnect user {user_id} was already registered in MaCantine with email {email}.")
            return user
        except get_user_model().DoesNotExist:
            pass

        # Create user
        last_name = user_data.get("usual_name")
        logger.info(f"Creating new user from ProConnect user {user_id} with email {email}.")
        user = get_user_model().objects.create(
            first_name=user_data.get("given_name"),
            last_name=last_name,
            email=email,
            proconnect_id=user_id,
            # phone_number=proconnect_data.get("phone"),
            username=f"{last_name}-proconnect-{user_id}",
            proconnect_organizations=organizations,
            created_with_proconnect=True,
        )
        return user

    @staticmethod
    def userinfo(token):
        """
        Authlib's method (callable as oauth.proconnect.userinfo(token=token))
        does not currently function with ProConnect tokens.
        There are issues with a non-configurable leeway and the structure of the token
        received by ProConnect.
        This method takes their function as of v1.3.2 and rewrites it to fix the
        issues manually. Inspired by:
        https://github.com/datagouv/udata-front/blob/f227ce5a8bba9822717ebd5986f5319f45e1622f/udata_front/views/proconnect.py#L29
        """
        metadata = oauth.proconnect.load_server_metadata()
        resp = oauth.proconnect.get(metadata["userinfo_endpoint"], token=token)
        resp.raise_for_status()
        # Create a new token that `client.parse_id_token` expects. Replace the initial
        # `id_token` with the jwt we received from the `userinfo_endpoint`.
        userinfo_token = token.copy()
        userinfo_token[ID_TOKEN_KEY] = resp.content
        user_data = oauth.proconnect.parse_id_token(userinfo_token, nonce=None)
        return user_data
