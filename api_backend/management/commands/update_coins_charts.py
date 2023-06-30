import json
import time
from django.conf import settings
from django.core.management.base import BaseCommand
import requests
from api_backend.models import PriceUpdate

coingecko = "https://api.coingecko.com/api/v3"
coins = "/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en"


class Command(BaseCommand):
    help = "Update the crypto databases"

    def handle(self, *args, **kwargs):

        response = requests.get(coingecko + coins)
        if response.status_code != 200:
            self.stdout.write(
                self.style.ERROR("Failed to retrieve data from the endpoint.")
            )
            return
        coin_data = response.json()
        for coin in coin_data:
            if settings.DEBUG:
                coin_id = coin["id"]
            try:
                response = requests.get(
                    f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=eur&days=365"
                )
            except BaseException:
                continue
            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR("Failed to retrieve data.")
                )
                continue
            coin = response.json()
            print(coin_id)
            # Extract relevant data from the coin object
            price_time = coin["prices"]

            try:
                coin_obj = PriceUpdate.objects.get(id=coin_id)
            except PriceUpdate.DoesNotExist:
                coin_obj = PriceUpdate(id=coin_id)

            # update
            coin_obj.price_time = json.dumps(price_time)

            coin_obj.save()
            time.sleep(6)  # to avoid max requests

        self.stdout.write(self.style.SUCCESS("Database update complete."))
