from django.urls import path
from .views import CoinDetailView, CryptoListView


urlpatterns = [
    path('', CryptoListView.as_view(), name='crypto_list'),
    path('<int:pk>/', CoinDetailView.as_view(), name='coin')
]