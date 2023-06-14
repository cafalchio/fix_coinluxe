from typing import Any, Dict
from django.views.generic import ListView, DetailView
from .models import Coins, CryptoCurrency
from django.db.models import Q


class CryptoListView(ListView):
    paginate_by = 15
    model = CryptoCurrency
    template_name = "api_backend/cryptos.html"
    
    def get_queryset(self):
        queryset =  CryptoCurrency.objects.order_by('-market_cap')
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(symbol__icontains=search_query)
            )

        return queryset
    
class CoinDetailView(DetailView):
    model = Coins
    template_name = "api_backend/coin.html"
    context_object = 'coin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coin = Coins.objects.get(id=self.kwargs.get("pk"))
        context['coin'] = coin
        return context

    