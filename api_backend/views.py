from django.views.generic import ListView, DetailView
from django.db.models import Q
import pandas as pd
from .utils import plot_chart
from .models import Coins, CryptoCurrency, PriceUpdate



class CryptoListView(ListView):
    paginate_by = 10
    model = CryptoCurrency
    template_name = "api_backend/cryptos.html"
    #

    def get_queryset(self):
        queryset = CryptoCurrency.objects.order_by('-market_cap')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get models data
        coin = Coins.objects.get(id=self.kwargs.get("pk"))
        price = PriceUpdate.objects.get(id=coin.id)
        crypto = CryptoCurrency.objects.get(id=coin.id)
        
        # processing data
        df = pd.DataFrame(price.formatted_price_time)
        df.columns = ["date", "price"]
        df.date = pd.to_datetime(df.date, unit='ms')
        chart = plot_chart(df)
        
        # contexts
        context['chart'] = chart
        context['coin'] = coin
        context['crypto'] = crypto

        return context
