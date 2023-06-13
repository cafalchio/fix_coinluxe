import asyncio
import aiohttp
import psycopg2
import os
import urllib.parse as up
from dotenv import load_dotenv

from coinluxe import settings

load_dotenv()


class CoinGecko:
    def __init__(self):
        self.host = "https://api.coingecko.com/api/v3"

    async def fetch_data(self, endpoint):
        """Method to fetch data from an endpoint."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.host + endpoint) as response:
                    data = await response.json()
                    return data
            except aiohttp.ClientError as e:
                print(f"An error occurred during the HTTP request: {e}")

    async def get_coin_market(self):
        """Method to get market data from a coin"""
        endpoint = '/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=250&page=1&sparkline=false&locale=en'
        data = await self.fetch_data(endpoint)
        return data


async def update_db():
    if settings.DEBUG:
        print("starting DB updated")
    url = up.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(database=url.path[1:],
                            user=url.username,
                            password=url.password,
                            host=url.hostname,
                            port=url.port)
    cur = conn.cursor()

    # Update the data in the table
    coingecko = CoinGecko()
    data = await coingecko.get_coin_market()
    if settings.DEBUG:
        print(f" dowloaded {len(data)} coins")
    if data:
        for entry in data:
            cur.execute("""
            UPDATE api_backend_cryptocurrency
            SET symbol = %s, name = %s, image = %s, current_price = %s, market_cap = %s,
                market_cap_rank = %s, fully_diluted_valuation = %s, total_volume = %s,
                high_24h = %s, low_24h = %s, price_change_24h = %s, price_change_percentage_24h = %s,
                market_cap_change_24h = %s, market_cap_change_percentage_24h = %s,
                circulating_supply = %s, total_supply = %s, max_supply = %s, ath = %s,
                ath_change_percentage = %s, ath_date = %s, atl = %s, atl_change_percentage = %s,
                atl_date = %s, last_updated = %s
            WHERE id = %s
            """, (
                entry['symbol'], entry['name'], entry['image'], entry.get(
                    'current_price'),
                entry.get('market_cap'), entry.get(
                    'market_cap_rank'), entry.get('fully_diluted_valuation'),
                entry.get('total_volume'), entry.get('high_24h'), entry.get(
                    'low_24h'), entry.get('price_change_24h'),
                entry.get('price_change_percentage_24h'), entry.get(
                    'market_cap_change_24h'),
                entry.get('market_cap_change_percentage_24h'), entry.get(
                    'circulating_supply'), entry.get('total_supply'),
                entry.get('max_supply'), entry.get('ath'), entry.get(
                    'ath_change_percentage'), entry.get('ath_date'),
                entry.get('atl'), entry.get('atl_change_percentage'), entry.get(
                    'atl_date'), entry['last_updated'],
                entry['id']
            ))
            # RUN FIRST TIME TO ADD VALUES TO THE DB
            # cur.execute("""
            # INSERT INTO api_backend_cryptocurrency (id, symbol, name, image, current_price, market_cap,
            #     market_cap_rank, fully_diluted_valuation, total_volume, high_24h, low_24h,
            #     price_change_24h, price_change_percentage_24h, market_cap_change_24h,
            #     market_cap_change_percentage_24h, circulating_supply, total_supply, max_supply,
            #     ath, ath_change_percentage, ath_date, atl, atl_change_percentage,
            #     atl_date, last_updated)
            # VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            # ON CONFLICT (id) DO NOTHING
            # """, (
            #     entry['id'], entry['symbol'], entry['name'], entry.get('image'), entry.get('current_price'),
            #     entry.get('market_cap'), entry.get('market_cap_rank'), entry.get('fully_diluted_valuation'),
            #     entry.get('total_volume'), entry.get('high_24h'), entry.get('low_24h'), entry.get('price_change_24h'),
            #     entry.get('price_change_percentage_24h'), entry.get('market_cap_change_24h'),
            #     entry.get('market_cap_change_percentage_24h'), entry.get('circulating_supply'), entry.get('total_supply'),
            #     entry.get('max_supply'), entry.get('ath'), entry.get('ath_change_percentage'), entry.get('ath_date'),
            #     entry.get('atl'), entry.get('atl_change_percentage'), entry.get('atl_date'), entry['last_updated']
            # ))

        # Commit the changes to the database
        conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    if settings.DEBUG:
        print("Db updated")
if __name__ == "__main__":
    asyncio.run(update_db())
