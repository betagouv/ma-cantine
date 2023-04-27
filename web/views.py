import logging
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import get_user_model, tokens, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from common.utils import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, FormView, View
from web.forms import RegisterUserForm
from data.factories import UserFactory
from django.views.decorators.clickjacking import xframe_options_exempt
from authlib.integrations.django_client import OAuth

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


class SampleOIDCLoginView(View):
    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri(reverse_lazy("oidc-authorize"))
        return oauth.moncomptepro.authorize_redirect(request, redirect_uri)


class SampleOIDCAuthorizeView(View):
    def get(self, request, *args, **kwargs):
        try:
            token = oauth.moncomptepro.authorize_access_token(request)
            mcp_data = oauth.moncomptepro.userinfo(token=token)
            user, created = self.get_or_create_user(mcp_data)

            if created:
                user.created_with_mcp = True
            if not user.mcp_id:
                user.mcp_id = mcp_data.get("sub")
            user.mcp_organizations = mcp_data.get("organizations")
            user.save()
            login(request, user)
            return redirect(reverse_lazy("app"))
        except Exception as e:
            logger.exception("Error authenticating with MonComptePro")
            logger.exception(e)
            return redirect("app")

    def get_or_create_user(self, mcp_data):
        mcp_id = mcp_data.get("sub")
        mcp_email = mcp_data.get("email")

        # Attempt with mcp_id
        try:
            user = get_user_model().objects.get(mcp_id=mcp_id)
            logger.info(f"MonComptePro user {mcp_id} (ID Ma Cantine: {user.id}) was found.")
            return user, False
        except get_user_model().DoesNotExist:
            logger.info(f"MonComptePro user {mcp_id} was not found.")

        # Attempt with email
        try:
            user = get_user_model().objects.get(email=mcp_email)
            logger.info(f"MonComptePro user {mcp_id} was already registered in MaCantine with email {mcp_email}.")
            return user, False
        except get_user_model().DoesNotExist:
            logger.info(f"MonComptePro user {mcp_id} ({mcp_email}) was not found on our database.")

        # Create user
        logger.info(f"Creating new user from MonComptePro user {mcp_id} with email {mcp_email}.")
        user = UserFactory.create(
            first_name=mcp_data.get("given_name"),
            last_name=mcp_data.get("family_name"),
            email=mcp_email,
            mcp_id=mcp_id,
            phone_number=mcp_data.get("phone_number"),
            username=f"{mcp_data.get('family_name')}-mcp-{mcp_id}",
            mcp_organizations=mcp_data.get("organizations"),
            created_with_mcp=True,
        )
        return user, True
