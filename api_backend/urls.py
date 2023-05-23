from django.urls import path
from .views import CryptoListView

urlpatterns = [
    path("cryptos/", CryptoListView.as_view(), name="cryptos"),
    # Other URL patterns
]
