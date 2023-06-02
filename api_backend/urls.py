from django.urls import path
from .views import CryptoListView

urlpatterns = [
    path("list/", CryptoListView.as_view(), name="cryptos"),
    # Other URL patterns
]
