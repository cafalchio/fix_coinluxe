from django.views.generic import ListView
from .models import CryptoCurrency

class CryptoListView(ListView):
    paginate_by = 25
    model = CryptoCurrency
    template_name = "api_backend/cryptos.html"
    
    def get_queryset(self):
        return CryptoCurrency.objects.order_by('-market_cap')