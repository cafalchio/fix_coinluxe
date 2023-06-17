from django.urls import path

from products.views import add_product, delete_product, edit_product
from .views import CoinDetailView, CryptoListView



urlpatterns = [
    path('', CryptoListView.as_view(), name='crypto_list'),
    path('<str:pk>/', CoinDetailView.as_view(), name='coin'),
    path('add/', add_product, name='add_product'),
    path('edit/<int:product_id>/', edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         delete_product,
         name='delete_product'),
]