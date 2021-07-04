from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, tokens, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.template import loader
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, FormView, View
from web.forms import RegisterForm, RegisterUserForm


class VueAppDisplayView(TemplateView):
    """
    This template contains the VueJS app in /frontend
    """

    template_name = "vue-app.html"


class RegisterView(FormView):
    """
    View containing the form to create an account
    """

    form_class = RegisterForm
    template_name = "auth/register.html"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        try:
            _login_and_send_activation_email(username, self.request)
        except Exception:
            self.success_url = reverse_lazy(
                "registration_email_sent_error", kwargs={"username": username}
            )
            return super().form_valid(form)
        else:
            self.success_url = reverse_lazy("app")
            return super().form_valid(form)


class RegisterUserView(FormView):
    """
    View containing the user-only form to create an account
    """

    form_class = RegisterUserForm
    template_name = "auth/register-user.html"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        try:
            _login_and_send_activation_email(username, self.request)
        except Exception:
            self.success_url = reverse_lazy(
                "registration_email_sent_error", kwargs={"username": username}
            )
            return super().form_valid(form)
        else:
            self.success_url = reverse_lazy("app")
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
            return redirect(
                reverse_lazy(
                    "registration_email_sent_error", kwargs={"username": username}
                )
            )


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
                "Votre compte est bien active, vous pouvez vous identifier.",
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
        html_template = "auth/account_activate_email.html"
        text_template = "auth/account_activate_email.txt"
        context = {
            "token": token,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "protocol": "https" if settings.SECURE_SSL_REDIRECT else "http",
            "domain": settings.HOSTNAME,
        }
        send_mail(
            subject="Activation de votre compte Ma Cantine",
            message=loader.render_to_string(text_template, context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=loader.render_to_string(html_template, context),
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect(reverse_lazy("app"))
    except Exception:
        raise Exception("Error occurred : the mail could not be sent.")
