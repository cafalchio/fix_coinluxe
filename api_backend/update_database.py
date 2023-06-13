from django.core.management.base import BaseCommand
import requests
from django.core.exceptions import ObjectDoesNotExist
from models import Coins, CryptoCurrency

coingecko = "https://api.coingecko.com/api/v3"
coins = '/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en'
# coin_detail = f'/coins/{coin}?localization=false&tickers=false&market_data=false&community_data=true&developer_data=true&sparkline=false'

class Command(BaseCommand):
    help = "Update the crypto databases"
    
    def handle(self, *args, **kwargs):
        
        response = requests.get(coingecko + coins)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to retrieve data from the endpoint.'))
            return
        coin_data = response.json()
        for coin in coin_data:
            # Extract relevant data from the coin object
            coin_id = coin['id']
            symbol = coin['symbol']
            name = coin['name']
            block_time_in_minutes = coin['block_time_in_minutes']
            categories = coin['categories']
            description = coin['description']
            homepage = coin['homepage']
            blockchain_site = coin['blockchain_site']
            market_cap_rank = coin['market_cap_rank']

            # Check if the coin already exists in the database
            try:
                coin_obj = Coins.objects.get(id=coin_id)
            except ObjectDoesNotExist:
                coin_obj = Coins(id=coin_id)

            # Update the coin object with the new data
            coin_obj.symbol = symbol
            coin_obj.name = name
            coin_obj.block_time_in_minutes = block_time_in_minutes
            coin_obj.categories = categories
            coin_obj.description = description
            coin_obj.homepage = homepage
            coin_obj.blockchain_site = blockchain_site
            coin_obj.market_cap_rank = market_cap_rank

            # Save the coin object in the database
            coin_obj.save()

        self.stdout.write(self.style.SUCCESS('Database update complete.'))

