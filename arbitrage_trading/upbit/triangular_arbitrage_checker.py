from upbit_module import *
import requests
import time

# Get list of cryptos for triangular arbitrage
def get_triangular_cryptos():
    try:
        cryptos = upbit_ticker_all()
        btc_market_exists = []

        for crypto in cryptos:
            ENDPOINT = f"https://api.upbit.com/v1/orderbook?markets=BTC-{crypto}"
            response = requests.get(ENDPOINT)
            if response.status_code != 404:
                btc_market_exists.append(crypto)

        btc_market_exists.sort()
        return btc_market_exists
    except Exception as e:
        print(f"Error fetching triangular cryptos: {e}")
        return []

# Constructing the URL with available cryptocurrencies for triangular arbitrage
def generate_triangular_url(available_cryptos):
    if not available_cryptos:
        print("No available cryptocurrencies for triangular arbitrage.")
        return ""

    try:
        url = "https://api.upbit.com/v1/orderbook?markets=KRW-BTC,"
        url += ",".join(f"KRW-{crypto},BTC-{crypto}" for crypto in available_cryptos)
        return url
    except Exception as e:
        print(f"Error generating triangular URL: {e}")
        return ""

start_time = time.time()

# List of available cryptocurrencies
def display_triangular_data():
    available_cryptos = get_triangular_cryptos()
    url = generate_triangular_url(available_cryptos)
    print(available_cryptos)
    print("_______")
    print(url)

    return available_cryptos, url

if __name__  == "__main__":
    display_triangular_data()
t

print("--- %s seconds ---" % (time.time() - start_time))
notify("done done done done check the url homie! ha!")
