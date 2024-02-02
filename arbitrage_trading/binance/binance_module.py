import requests
from pprint import pprint
from arbitrage_trading.config import *
import pandas as pd



# Live price data
def binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url)
        return float(response.json()["price"])
    except Exception as e:
        print(e)
        raise SystemExit("Binance API banned in US IP")



# Risk Management
# - Hedge by adjusting short position size with leverage.
# - Adjust the minimum position size of crypto worth $5.021 with leverage.
# - Caution: High leverage when hedging may lead to potential blow-ups.
def Hedge(exchange, symbol, exchange_order):
    # # Hedge
    # KRW = 6016.419949
    # leverage,size = Hedge("upbit",symbol,KRW)

    #  Set initial cash for calculation
    MIN_ORDER = 6
    if exchange == "upbit":  # KRW -> USD
        exchange_order = exchange_order / get_currency_api("USD")

    # Calculate Leverage
    LEVERAGE = round(exchange_order / MIN_ORDER)
    if LEVERAGE == 0:  # x0 -> x1
        LEVERAGE = 1

    # Calculate minimum position size
    MIN_SIZE = MIN_ORDER / binance_futures_test.fetch_ticker(f"{symbol}/USDT")["last"]

    # Hedge
    try:
        binance_futures_test.set_leverage(LEVERAGE, f"{symbol}/USDT")
        pprint(
            binance_futures_test.create_market_sell_order(f"{symbol}/USDT", MIN_SIZE)
        )
        print("Hedged!")
        print(f"Leverage : {LEVERAGE}, size : {MIN_SIZE}")
    except Exception as e:
        print(e)

    return LEVERAGE, MIN_SIZE


def UnHedge(symbol, leverage, size):
    # # UnHedge
    # UnHedge(symbol,leverage,size)

    try:
        pprint(binance_futures_test.create_market_buy_order(f"{symbol}/USDT", size))
        print("Unhedged!")
        print(f"Leverage : {leverage}, size : {size}")
    except Exception as e:
        print(e)


# Backtest Modules
def binance_test(symbol, period):
    bnc_ohlcv = binance.fetch_ohlcv(f"{symbol}/USDT", period)
    df = pd.DataFrame(
        bnc_ohlcv, columns=["datetime", "open", "high", "low", "close", "volume"]
    )
    df.set_index("datetime", inplace=True)
    return df




