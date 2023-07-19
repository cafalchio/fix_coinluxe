from django.urls import path
from .views import IndexListView, test_view

urlpatterns = [
    path("", IndexListView.as_view(), name="home"),
    path("loaderio-f7cb4845fcb26f88ba745418682e372e.txt", test_view, name="test-view"),
]

