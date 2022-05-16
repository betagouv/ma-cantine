from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path
from magicauth.urls import urlpatterns as magicauth_urls
from web.views import VueAppDisplayView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]
urlpatterns.append(re_path(r"", include("web.urls")))
urlpatterns.append(re_path(r"^api/v1/", include("api.urls")))


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_PERFORMANCE:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)


urlpatterns.extend(magicauth_urls)

# In order for vue-history to work in HTML5 mode, we need to add a catch-all
# route returning the app (https://router.vuejs.org/guide/essentials/history-mode.html#html5-history-mode)
urlpatterns.append(re_path(r"^.*/$", VueAppDisplayView.as_view()))

admin.site.site_header = f"Ma Cantine EGALIM - {getattr(settings, 'ENVIRONMENT', '')}"
admin.site.index_title = ""
admin.site.site_title = f"Ma Cantine EGALIM - {getattr(settings, 'ENVIRONMENT', '')}"
