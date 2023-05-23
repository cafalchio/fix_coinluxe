import asyncio
from coingecko_api import CoinGecko
from api_backend.models import CryptoCurrency


async def update_crypto_currencies():
    coingecko = CoinGecko()
    data = await coingecko.get_coin_market()

    if data:
        for crypto in data:
            crypto_id = crypto['id']
            symbol = crypto['symbol']
            name = crypto['name']
            image = crypto.get('image', None)
            current_price = crypto.get('current_price', 0.0)
            market_cap = crypto.get('market_cap', 0)
            market_cap_rank = crypto.get('market_cap_rank', 0)
            fully_diluted_valuation = crypto.get(
                'fully_diluted_valuation', None)
            total_volume = crypto.get('total_volume', 0)
            high_24h = crypto.get('high_24h', 0.0)
            low_24h = crypto.get('low_24h', 0.0)
            price_change_24h = crypto.get('price_change_24h', 0.0)
            price_change_percentage_24h = crypto.get(
                'price_change_percentage_24h', 0.0)
            market_cap_change_24h = crypto.get('market_cap_change_24h', 0.0)
            market_cap_change_percentage_24h = crypto.get(
                'market_cap_change_percentage_24h', 0.0)
            circulating_supply = crypto.get('circulating_supply', None)
            total_supply = crypto.get('total_supply', None)
            max_supply = crypto.get('max_supply', None)
            ath = crypto.get('ath', 0.0)
            ath_change_percentage = crypto.get('ath_change_percentage', 0.0)
            ath_date = crypto.get('ath_date', None)
            atl = crypto.get('atl', 0.0)
            atl_change_percentage = crypto.get('atl_change_percentage', 0.0)
            atl_date = crypto.get('atl_date', None)
            roi = crypto.get('roi', None)
            last_updated = crypto.get('last_updated', None)

            # Check if the CryptoCurrency instance already exists
            try:
                crypto_currency = CryptoCurrency.objects.get(id=crypto_id)
                # Update the fields of the existing instance
                crypto_currency.symbol = symbol
                crypto_currency.name = name
                crypto_currency.image = image
                crypto_currency.current_price = current_price
                crypto_currency.market_cap = market_cap
                crypto_currency.market_cap_rank = market_cap_rank
                crypto_currency.fully_diluted_valuation = fully_diluted_valuation
                crypto_currency.total_volume = total_volume
                crypto_currency.high_24h = high_24h
                crypto_currency.low_24h = low_24h
                crypto_currency.price_change_24h = price_change_24h
                crypto_currency.price_change_percentage_24h = price_change_percentage_24h
                crypto_currency.market_cap_change_24h = market_cap_change_24h
                crypto_currency.market_cap_change_percentage_24h = market_cap_change_percentage_24h
                crypto_currency.circulating_supply = circulating_supply
                crypto_currency.total_supply = total_supply
                crypto_currency.max_supply = max_supply
                crypto_currency.ath = ath
                crypto_currency.ath_change_percentage = ath_change_percentage
                crypto_currency.ath_date = ath_date
                crypto_currency.atl = atl
                crypto_currency.atl_change_percentage = atl_change_percentage
                crypto_currency.atl_date = atl_date
                crypto_currency.roi = roi
                crypto_currency.last_updated = last_updated
                crypto_currency.save()
            except CryptoCurrency.DoesNotExist:
                # Create a new CryptoCurrency instance
                CryptoCurrency.objects.create(
                    id=crypto_id,
                    symbol=symbol,
                    name=name,
                    image=image,
                    current_price=current_price,
                    market_cap=market_cap,
                    market_cap_rank=market_cap_rank,
                    fully_diluted_valuation=fully_diluted_valuation,
                    total_volume=total_volume,
                    high_24h=high_24h,
                    low_24h=low_24h,
                    price_change_24h=price_change_24h,
                    price_change_percentage_24h=price_change_percentage_24h,
                    market_cap_change_24h=market_cap_change_24h,
                    market_cap_change_percentage_24h=market_cap_change_percentage_24h,
                    circulating_supply=circulating_supply,
                    total_supply=total_supply,
                    max_supply=max_supply,
                    ath=ath,
                    ath_change_percentage=ath_change_percentage,
                    ath_date=ath_date,
                    atl=atl,
                    atl_change_percentage=atl_change_percentage,
                    atl_date=atl_date,
                    roi=roi,
                    last_updated=last_updated
                )


def update_crypto_currency_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_crypto_currencies())


if __name__ == "__main__":
    update_crypto_currency_data()
