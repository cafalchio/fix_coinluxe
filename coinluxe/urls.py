from django.contrib import admin
from django.urls import include, path
from coinluxe import settings
from home.views import index 
from theme.views import change_theme
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),
    path('switch-theme/' , change_theme, name='change_theme'),
    path("", index, name="home")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
