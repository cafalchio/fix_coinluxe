from django.views.generic import ListView
from .models import CryptoCurrency


class CryptoListView(ListView):
    model = CryptoCurrency
    template_name = "cryptos.html"
    context_object_name = "cryptos"
    paginate_by = 10  # Number of items to display per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Sort by price if the 'sort' parameter is 'price', otherwise sort by market_cap
        sort_param = self.request.GET.get('sort')
        if sort_param == 'price':
            queryset = queryset.order_by('price')
        else:
            queryset = queryset.order_by('market_cap')

        return queryset
