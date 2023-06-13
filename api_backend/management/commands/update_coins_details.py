import time
from django.core.management.base import BaseCommand
import requests
from api_backend.models import Coins

coingecko = "https://api.coingecko.com/api/v3"
coins = '/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en'

class Command(BaseCommand):
    help = "Update the crypto databases"
    
    def handle(self, *args, **kwargs):
        
        response = requests.get(coingecko + coins)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to retrieve data from the endpoint.'))
            return
        coin_data = response.json()
        
        for coin in coin_data:
            coin_id = coin['id']
            response = requests.get(coingecko + f'/coins/{coin_id}?localization=false&tickers=false&market_data=false&community_data=true&developer_data=true&sparkline=false')
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR('Failed to retrieve data from the endpoint.'))
                return
            coin = response.json()
            
            # Extract relevant data from the coin object
            coin_id = coin['id']
            symbol = coin["symbol"]
            name = coin["name"]
            block_time_in_minutes = coin['block_time_in_minutes']
            categories = coin.get("categories", [])  
            description = "coin_description"
            homepage = coin.get("homepage", []) 
            blockchain_site = coin.get("blockchain_site", [])  
            market_cap_rank = 1
            homepage_value = homepage[0] if homepage else None
            blockchain_site_value = blockchain_site[0] if blockchain_site else None
            categories_value = categories[0] if categories else None

            try:
                coin_obj = Coins.objects.get(id=coin_id)
            except Coins.DoesNotExist:
                coin_obj = Coins(id=coin_id)
                
            # update
            coin_obj.symbol = symbol
            coin_obj.name = name
            coin_obj.block_time_in_minutes = block_time_in_minutes
            coin_obj.categories = categories_value
            coin_obj.description = description
            coin_obj.homepage = homepage_value
            coin_obj.blockchain_site = blockchain_site_value
            coin_obj.market_cap_rank = market_cap_rank

            coin_obj.save()
            time.sleep(8) # to avoid max requests

        self.stdout.write(self.style.SUCCESS('Database update complete.'))

