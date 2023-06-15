import json
from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView, DetailView
import pandas as pd
from .models import Coins, CryptoCurrency, PriceUpdate
from django.db.models import Q
import plotly.express as px
from .forms import DateForm


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
    context_object_name = 'coin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the coin object
        coin = self.object

        # Perform necessary data processing and chart creation
        coin = Coins.objects.get(id=self.kwargs.get("pk"))
        price = PriceUpdate.objects.get(id=coin.id)
        df = pd.DataFrame(price.formatted_price_time)
        df.columns = ["date", "price"]
        df.date = pd.to_datetime(df.date, unit='ms')
        print(df.head())
        fig = px.line(
            x=df.date,
            y=df.price,
            title=f"{coin} Price €",

            labels={'x': 'Date', 'y': 'Price €'}
        )
        fig.update_layout(
            title={
                'font_size': 24,
                'xanchor': 'center',
                'x': 0.5
            },
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
        )
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        fig.update_layout(modebar_remove=[
                          'zoom', 'pan', 'select', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d', 'toImage'])
        fig.update_layout()
        config = {'displayModeBar': False, 'displaylogo': False}

        chart = fig.to_html(config)
        with open("fig.html", "w") as f:
            f.write(chart)
        

        # Create and add the form to the context
        form = DateForm()
        context['form'] = form

        # Add the chart and coin object to the context
        context['chart'] = chart
        context['coin'] = coin

        return context
