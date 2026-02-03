from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from web.sitemaps import BlogPostSitemap, CanteenSitemap, PartnerSitemap, WebSitemap
from web.views import (
    AccountActivationView,
    ActivationTokenView,
    LoginUserView,
    OIDCAuthorizeView,
    OIDCLoginView,
    RegisterDoneView,
    RegisterInvalidTokenView,
    RegisterSendMailFailedView,
    RegisterUserView,
    VueAppDisplayView,
    WidgetView,
)

sitemaps = {
    "canteens": CanteenSitemap,
    "blog": BlogPostSitemap,
    "partners": PartnerSitemap,
    "other": WebSitemap,
}

urlpatterns = [
    re_path(r"^widgets/.*$", WidgetView.as_view(), name="widget_app"),
    path("", VueAppDisplayView.as_view(), name="app"),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.LoginView
    path(
        "s-identifier",
        LoginUserView.as_view(
            template_name="auth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.LogoutView
    path(
        "se-deconnecter",
        auth_views.LogoutView.as_view(
            template_name="auth/logged_out.html",
        ),
        name="logout",
    ),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordChangeView
    path(
        "modification-mot-de-passe",
        auth_views.PasswordChangeView.as_view(
            template_name="auth/password_change_form.html",
        ),
        name="password_change",
    ),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordChangeDoneView
    path(
        "mot-de-passe-modifie",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="auth/password_change_done.html",
        ),
        name="password_change_done",
    ),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetView
    path(
        "reinitialisation-mot-de-passe",
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset_form.html",
        ),
        name="password_reset",
    ),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetDoneView
    path(
        "email-reinitialisation-envoye",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetConfirmView
    path(
        "nouveau-mot-de-passe/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    # https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordResetCompleteView
    path(
        "mot-de-passe-reinitialise",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    # Views allowing the creation of an account
    path("creer-mon-compte", RegisterUserView.as_view(), name="register"),
    path(
        "nouvel-utilisateur",
        RedirectView.as_view(url="/creer-mon-compte"),
        name="register_user",
    ),
    path(
        "email-de-confirmation",
        ActivationTokenView.as_view(),
        name="registration_email",
    ),
    path(
        "email-de-confirmation-envoye/<username>",
        RegisterDoneView.as_view(),
        name="registration_email_sent",
    ),
    path(
        "email-de-confirmation-non-envoye/<username>",
        RegisterSendMailFailedView.as_view(),
        name="registration_email_sent_error",
    ),
    path(
        "activation-compte/<uidb64>/<token>",
        AccountActivationView.as_view(),
        name="activate",
    ),
    path("token-invalide", RegisterInvalidTokenView.as_view(), name="invalid_token"),
    path(
        "sitemap.xml",
        cache_page(60 * 60)(sitemap),
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    path(
        "googlefbd6f06a151f47ee.html",
        TemplateView.as_view(template_name="googlefbd6f06a151f47ee.html"),
        name="google_verification",
    ),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "swagger-ui/",
        RedirectView.as_view(pattern_name="swagger-ui", permanent=True),
        name="swagger-ui-old",
    ),
]

if settings.USES_MONCOMPTEPRO:
    urlpatterns.append(
        path(
            "oidc-login",
            OIDCLoginView.as_view(),
            name="oidc-login",
        )
    )

    urlpatterns.append(
        path(
            "signin-oidc",
            OIDCAuthorizeView.as_view(),
            name="oidc-authorize",
        )
    )
