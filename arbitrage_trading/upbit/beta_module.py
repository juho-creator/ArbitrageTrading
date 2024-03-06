from upbit_module import *
import requests
import time

def get_triangular_cryptos():
    cryptos = upbit_ticker_all()
    btc_market_exists = []

    for crypto in cryptos:
        ENDPOINT = f"https://api.upbit.com/v1/orderbook?markets=BTC-{crypto}"
        response = requests.get(ENDPOINT)
        if response.status_code != 404:
            btc_market_exists.append(crypto)
    return btc_market_exists



start_time = time.time()

# List of available cryptocurrencies
available_cryptos = get_triangular_cryptos()

# Constructing the URL with available cryptocurrencies for triangular arbitrage
url = "https://api.upbit.com/v1/orderbook?markets="
url += ",".join(f"KRW-{crypto},BTC-{crypto}" for crypto in available_cryptos)
print(url)

print("--- %s seconds ---" % (time.time() - start_time))
notify("done done done done check the url homie! ha!")