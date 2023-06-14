from typing import Any, Dict
from django.views.generic import ListView, DetailView
from .models import Coins, CryptoCurrency


class CryptoListView(ListView):
    paginate_by = 25
    model = CryptoCurrency
    template_name = "api_backend/cryptos.html"
    
    def get_queryset(self):
        return CryptoCurrency.objects.order_by('-market_cap')
    
class CoinDetailView(DetailView):
    model = Coins
    template_name = "api_backend/coin.html"
    context_object = 'coin'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        coin = Coins.objects.filter(id=self.kwargs.get("id"))
        return context

    