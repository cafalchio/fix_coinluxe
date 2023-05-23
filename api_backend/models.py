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

    def __str__(self):
        return self.name
