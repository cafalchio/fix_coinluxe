from django.contrib import admin
from django.urls import include, path
from coinluxe import settings
from home.views import index
from theme.views import change_theme
from api_backend.views import CryptoListView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),
    path('switch-theme/', change_theme, name='change_theme'),
    path("", index, name="home"),
    path("cryptos/list/",
         CryptoListView.as_view(template_name="api_backend/cryptos.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
