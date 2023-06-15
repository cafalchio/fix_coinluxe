from datetime import timedelta
import json
from django.db import models






class CryptoCurrency(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    image = models.URLField(null=True)
    current_price = models.FloatField(null=True)
    market_cap = models.BigIntegerField(null=True)
    market_cap_rank = models.PositiveIntegerField(null=True)
    fully_diluted_valuation = models.BigIntegerField(null=True)
    total_volume = models.BigIntegerField(null=True)
    high_24h = models.FloatField(null=True)
    low_24h = models.FloatField(null=True)
    price_change_24h = models.FloatField(null=True)
    price_change_percentage_24h = models.FloatField(null=True)
    market_cap_change_24h = models.FloatField(null=True)
    market_cap_change_percentage_24h = models.FloatField(null=True)
    circulating_supply = models.FloatField(null=True)
    total_supply = models.FloatField(null=True)
    max_supply = models.FloatField(null=True)
    ath = models.FloatField(null=True)
    ath_change_percentage = models.FloatField(null=True)
    ath_date = models.DateTimeField(null=True)
    atl = models.FloatField(null=True)
    atl_change_percentage = models.FloatField(null=True)
    atl_date = models.DateTimeField(null=True)
    last_updated = models.DateTimeField()

    @property
    def formatted_current_price(self):
        return '{:,.2f}'.format(self.current_price)

    @property
    def formatted_market_cap(self):
        if self.market_cap >= 1000000000:
            return '{:,.2f} bi'.format(self.market_cap / 1000000000)
        elif self.market_cap >= 1000000:
            return '{:,.2f} mi'.format(self.market_cap / 1000000)
        else:
            return '{:,.2f}'.format(self.market_cap)
        
    @property
    def formatted_price_change_24h(self):
        return f"{self.price_change_percentage_24h:.2f}%"
    
    @property
    def formatted_symbol(self):
        return f"{self.symbol.upper()}"
    
    
    @property 
    def formatted_last_updated(self):
        updated_time = self.last_updated + timedelta(hours=1)
        return updated_time.strftime("%m %b - %H:%M:%S")
        
    @property
    def formatted_total_volume(self):
        if self.total_volume >= 1000000000:
            return '{:,.2f} bi'.format(self.total_volume / 1000000000)
        elif self.total_volume >= 1000000:
            return '{:,.2f} mi'.format(self.total_volume / 1000000)
        else:
            return '{:,.2f}'.format(self.total_volume)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-market_cap']

    def __str__(self):
        return self.name


# Coin Detail
class Coins(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    symbol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    block_time_in_minutes = models.PositiveIntegerField(default=0, null=True)
    description = models.TextField(null=True)
    homepage = models.JSONField(max_length=100, null=True)
    blockchain_site = models.JSONField(max_length=100, null=True)
    market_cap_rank = models.PositiveIntegerField(default=0)
    categories = models.JSONField(max_length=100, null=True)

    @property
    def formatted_symbol(self):
        return f"{self.symbol.upper()}"
    
    @property
    def formatted_homepages(self):
        homepage_list = json.loads(self.homepage)
        return homepage_list[0]
    
    @property
    def formatted_categories(self):
        categories = json.loads(self.categories)
        return categories[0]
    
    @property
    def formatted_blockchain_site(self):
        blockchain_site = json.loads(self.blockchain_site)
        return blockchain_site[0]

    def __str__(self):
        return self.name
    
    
    
    class PriceUpdate(models.Model):
        coin = models.ForeignKey('Coins', on_delete=models.CASCADE)
        price_time = models.JSONField(max_length=365, null=True)

        def __str__(self):
            return f"Coin: {self.coin}, Price: {self.price}, Date: {self.date}"