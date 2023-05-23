import aiohttp
import os


class CoinGecko:
    def __init__(self):
        self.host = "https://api.coingecko.com/api/v3"

    async def fetch_data(self, endpoint):
        """Method to fetch data from an endpoint.

        Inputs:
            endpoint (str): The endpoint to get data from.

        Returns:
            dict: The JSON data from the response.

        Raises:
            aiohttp.ClientError: If there is an error with the HTTP request.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.host + endpoint) as response:
                    data = await response.json()
                    return data
            except aiohttp.ClientError as e:
                print(f"An error occurred during the HTTP request: {e}")

    async def get_coin_market(self):
        """Method to get market data from a coin

        Inputs:
            id_list (str): The list of crypto ids
            currency (str): The currency to get the value of the coin
        Returns: 
            data (json): the json price of the coin
        """
        endpoint = '/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en'
        data = await self.fetch_data(endpoint)
        return data
