from ..binance.binance_module import binance_price
from ..bithumb.bithumb_module import bithumb_price
from .upbit_arbitrage import one_way,other_way
import pandas as pd
import requests
import time
from pprint import pprint
from bs4 import BeautifulSoup


# Obtaining currency
def get_currency_api(code):
    try:
        url = (
            f"https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRW{code}"
        )
        response = requests.get(url).json()
        currency = response[0]["basePrice"]
        return currency
    except:
        print("Unable to retrieve currency")

def get_currency_web_scraping(code):
    try:
        url = f"https://m.stock.naver.com/marketindex/exchange/FX_{code}KRW"
        headers = {"Accept-Language": "ko-KR", "User-Agent": "Mozilla/5.0"}

        # HTTP request & response from Naver
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing HTML response data with lxml for better performance
            soup = BeautifulSoup(response.content, "lxml")

            # Extract exchange rate using a more specific selector
            exchange_rate_tag = soup.select_one("strong.DetailInfo_price__I_VJn")

            # Check if the tag is found
            if exchange_rate_tag:
                # Extract text from the tag and clean it up
                exchange_rate = (
                    exchange_rate_tag.get_text(strip=True)
                    .replace("KRW", "")
                    .replace(",", "")
                )

                # Convert the cleaned-up string to a float
                exchange_rate = float(exchange_rate)
                # print(f"{currency_code}KRW = {exchange_rate}")
                return exchange_rate
    except:
        print("Unable to retrieve currency")



# Retrive price
def upbit_price(symbol):
    try:
        url = f"https://api.upbit.com/v1/ticker?markets={symbol}"
        response = requests.get(url)
        data = response.json()[0]
        return float(data["trade_price"])
    except:
        print(f"Unable to get {symbol} price")

def upbit_global_price(symbol,country):
    try:
        if country == "SG":
            url = f"https://sg-api.upbit.com/v1/ticker?markets=SGD-{symbol}" # UPBIT Singapore
        elif country == "TH":
            url = f"https://th-api.upbit.com/v1/ticker?markets=THB-{symbol}" # UPBIT Thailand
        elif country == "ID":
            url = f"https://id-api.upbit.com/v1/ticker?markets=IDR-{symbol}" # UPBIT Indonesia

        response = requests.get(url)
        data = response.json()[0]
        return float(data["trade_price"])
    except:
        print(f"Unable to get {symbol} price from {country}")


# Get all ticker symbols
def upbit_ticker_all():
    url = "https://api.upbit.com/v1/market/all"

    resp = requests.get(url)
    data = resp.json()

    krw_tickers = [
        coin["market"][4:] for coin in data if coin["market"].startswith("KRW")
    ]

    return krw_tickers

def upbit_global_ticker_all(country):
    if country == "SG":
        url = "https://sg-api.upbit.com/v1/market/all"

    elif country == "ID":
        url = "https://id-api.upbit.com/v1/market/all"
    elif country == "TH":
        url = "https://th-api.upbit.com/v1/market/all"

    resp = requests.get(url)
    data = resp.json()  # UPBIT Singapore
    return data

# Transfer Arbitrage
def current_kimpga(symbol, currency):
    try:
        binance = binance_price(symbol)
        upbit = upbit_price(f"KRW-{symbol}")

        foreign_exchange = binance * currency

        if upbit > foreign_exchange:
            kimp = round(((upbit / foreign_exchange) - 1) * 100, 2)
            print(f"KIMP: {kimp}\t Binance : {binance}\t UPBIT :{upbit}\n")
            return kimp, binance, upbit

        elif foreign_exchange > upbit:
            kimp = round(((foreign_exchange / upbit) - 1) * 100, 2)
            print(f"KIMP: {kimp}\t Binance : {binance}\t UPBIT :{upbit}\n")
            return kimp, binance, upbit

    except:
        print(f"Unable to compute Kimp")

def get_all_kimp():
    df = pd.DataFrame()

    currency = get_currency_api("USD")

    for crypto in upbit_ticker_all():
        try:
            print(f"\n{crypto}")
            kimp, binance, upbit = current_kimpga(crypto, currency)
            data = {"symbol": crypto, "KIMP": kimp, "Binance": binance, "UPBIT": upbit}
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        except:
            print(f"{crypto} doesn't exist on binance")
    df.to_csv("output.csv", index=False)


if __name__== "__main__":
    start_time = time.time()
    print("hi")
    print("--- %s seconds ---" % (time.time() - start_time))
