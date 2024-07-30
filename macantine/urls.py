from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path
from magicauth.urls import urlpatterns as magicauth_urls
from web.views import VueAppDisplayView, Vue3AppDisplayView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from cms.api import api_router

urlpatterns = [
    path("admin/", admin.site.urls),  # if the path of 'admin/' changes, update historical_record_add_auth_method
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("apicms/v1/", api_router.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("pages/", include(wagtail_urls)),
]
urlpatterns.append(re_path(r"", include("web.urls")))
urlpatterns.append(re_path(r"^api/v1/", include("api.urls")))


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # a hack to get icon URLs to work in Vue 3 CSS
    urlpatterns += static("/2024-frontend/node_modules/@gouvfr/dsfr/dist/icons", document_root="static/dsfr/icons")

urlpatterns += (path("", include("django_vite_plugin.urls")),)

if settings.DEBUG_PERFORMANCE:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)


urlpatterns.extend(magicauth_urls)

# In order for vue-history to work in HTML5 mode, we need to add a catch-all
# route returning the app (https://router.vuejs.org/guide/essentials/history-mode.html#html5-history-mode)
if settings.ENABLE_VUE3:
    urlpatterns.append(re_path(r"^v2/.*$", Vue3AppDisplayView.as_view()))
urlpatterns.append(re_path(r"^.*/$", VueAppDisplayView.as_view()))

admin.site.site_header = f"Ma Cantine EGALIM - {getattr(settings, 'ENVIRONMENT', '')}"
admin.site.index_title = ""
admin.site.site_title = f"Ma Cantine EGALIM - {getattr(settings, 'ENVIRONMENT', '')}"
