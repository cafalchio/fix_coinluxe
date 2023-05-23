from django.views.generic import ListView
from api_backend.models import CryptoCurrency


class CryptoListView(ListView):
    model = CryptoCurrency
    template_name = "cryptos.html"
    context_object_name = "cryptos"
