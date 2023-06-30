from django.contrib import admin
from django.urls import include, path
from coinluxe import settings
from theme.views import change_theme

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("switch-theme/", change_theme, name="change_theme"),
    path("", include("home.urls")),
    path("cryptos/", include("api_backend.urls")),
    path("portifolio/", include("portifolio.urls")),
    path("products/", include("products.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "coinluxe.views.handler404"
