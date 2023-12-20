import config
import csv
from binance import Client
import requests

def get_binance_candlestick_data(symbol, interval, start_date, end_date):
    # Initialize Binance client
    client = Client(config.API_KEY, config.API_SECRET)

    # Get historical candlestick data
    candles = client.get_historical_klines(symbol, interval, start_date, end_date)

    # Open CSV File
    csvfile = open(f"binance_{symbol}.csv", 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    # Add header
    candlestick_writer.writerow([
        "Kline open time",
        "Open price",
        "High price",
        "Low price",
        "Close price",
        "Volume",
        "Kline Close time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
        "Unused field, ignore"
    ])

    # Write information
    for candlestick in candles:
        candlestick[0] = candlestick[0] / 1000
        candlestick_writer.writerow(candlestick)

    csvfile.close()



def get_upbit_candlestick(symbol, interval, start_date, end_date):
    market = f"KRW-{symbol}"
    url = f"https://api.upbit.com/v1/candles/{interval}?market={market}&count=1000&from={start_date}T00:00:00Z&to={end_date}T23:59:59Z"
    print(url)

    headers = {"accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    candlestick_data = response.json()

    # Open CSV File
    csvfile = open(f'upbit_{symbol}_{interval.replace("/", "")}.csv', 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')
    
    # Add header
    candlestick_writer.writerow([
        "market",
        "candle_date_time_utc",
        "candle_date_time_kst",
        "opening_price",
        "high_price",
        "low_price",
        "trade_price",
        "timestamp",
        "candle_acc_trade_price",
        "candle_acc_trade_volume",
        "unit"
    ])
    
    # Write information
    for candle in candlestick_data:
        candlestick_writer.writerow([
            candle["market"],
            candle["candle_date_time_utc"],
            candle["candle_date_time_kst"],
            candle["opening_price"],
            candle["high_price"],
            candle["low_price"],
            candle["trade_price"],
            candle["timestamp"],
            candle["candle_acc_trade_price"],
            candle["candle_acc_trade_volume"],
            candle["unit"]
        ])
    
    csvfile.close()



# # Sample initial values
# balance = 1000
# currency = "USD"
# symbol_upbit = "XRP"
# symbol_binance = "BTCUSDT"
# interval_binance = "1d"
# start_date = "2023-01-01"
# end_date = "2023-12-31"
# delay = 5  # in seconds



# # Example usage:
    
# import time
# start_time = time.time()
# # get_binance_candlestick_data("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 Jan, 2020", "2 Jan, 2020")
# get_upbit_candlestick(symbol_upbit, "minutes/1", start_date, end_date)

# print("--- %s seconds ---" % (time.time() - start_time))

import pyupbit
symbol = "BTC"


# 끝나는 시간 입력 = UTC,  출력 = KST
df = pyupbit.get_ohlcv(ticker=f"KRW-{symbol}", interval="minute1", count=10,to="2023-12-20 6:10:00")
# 간단히 pyupbit.get_ohlcv("KRW-BTC", "day", 10)으로 써도 똑같이 동작
print(df)

df.to_csv(f"upbit_{symbol}.csv")
