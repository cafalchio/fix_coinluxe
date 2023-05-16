from django.contrib import admin
from django.urls import include, path
from home.views import index 
from theme.views import change_theme

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),
    path('switch-theme/' , change_theme, name='change_theme'),
    path("", index, name="home")
]
