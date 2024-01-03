import config
import csv
from binance import Client
import datetime
import requests
from module import get_currency
import pandas as pd

def write_candlestick_row(candle, writer):
    # Format Open Time
    candle["candle_date_time_kst"] = datetime.datetime.strptime(candle["candle_date_time_kst"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

    # Format Close Time (in milliseconds)
    milliseconds = candle["timestamp"] / 1000

    # Timestamp -> Datetime
    candle["timestamp"] = (datetime.datetime.utcfromtimestamp(milliseconds) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

    writer.writerow([
        candle["candle_date_time_kst"],
        candle["opening_price"],
        candle["high_price"],
        candle["low_price"],
        candle["trade_price"],
        candle["candle_acc_trade_volume"],
        candle["timestamp"],
    ])

def get_binance_candlestick_data(symbol, interval, start_date, end_date):
    # Initialize Binance client
    client = Client(config.API_KEY, config.API_SECRET)
    
    # Dateformat -> Unixtimestamp (convert to current standard timezone)
    start_date = str(datetime.datetime.strptime(start_date, "%d %b, %Y").timestamp())
    end_date = str(datetime.datetime.strptime(end_date, "%d %b, %Y").timestamp())

    # Get historical candlestick data
    candles = client.get_historical_klines(symbol+"USDT", interval, start_date, end_date)

    # Open CSV File
    csvfile = open(f"binance_{symbol}.csv", 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    # Add header
    candlestick_writer.writerow([
        "Open time",
        "Open price",
        "High price",
        "Low price",
        "Close price",
        "Volume",
        "Close time"
    ])

    # Drop the last candle
    candles = candles[:-1]
    # Write information
    for candlestick in candles:
        candlestick = candlestick[:-5]

        # milliseconds => seconds
        milliseconds_open = candlestick[0] / 1000
        milliseconds_close = float(candlestick[-1]) / 1000
        

        # Unixformat -> DateTime (for Readability)
        date_format_open = (datetime.datetime.utcfromtimestamp(milliseconds_open) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
        date_format_close = (datetime.datetime.utcfromtimestamp(milliseconds_close) + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

        candlestick[0] = date_format_open
        candlestick[-1] = date_format_close

        candlestick_writer.writerow(candlestick)

    csvfile.close()

def get_upbit_candlestick(symbol, interval, start_date, end_date):
    MAX_API_CALL = 200

    # Convert date strings to datetime objects (UTC -> KST)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S") - datetime.timedelta(hours=9) 
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S") - datetime.timedelta(hours=9)

    # Calculate days difference
    days = (end_date - start_date).days

    # Calculate count based on days difference, with a maximum of MAX_API_CALL
    total_request = 1440 * days
    
    # Creating CSV File
    csv_filename = f'upbit_{symbol}.csv'
    market = f"KRW-{symbol}"
    headers = {"accept": "application/json"}

    # Set up initial headers
    with open(csv_filename, 'w', newline='') as csvfile:
        candlestick_writer = csv.writer(csvfile, delimiter=',')
        
        # Add header
        candlestick_writer.writerow([
            "Open time",
            "Open price",
            "High price",
            "Low price",
            "Close price",
            "Volume",
            "Close time",
        ])

        # Break down into multiple API request sessions if necessary 
        max_req_count = int(total_request / MAX_API_CALL)
        remaining_req_count = total_request - (MAX_API_CALL * max_req_count)

        # Make 200 API calls at a time
        for i in range(max_req_count):
            url = f"https://api.upbit.com/v1/candles/{interval}?market={market}&count={200}&to={end_date.strftime('%Y-%m-%dT%H:%M:%S')}"
            response = requests.get(url, headers=headers)
            candlestick_data = response.json()
            end_date = end_date - datetime.timedelta(minutes=200)

            # Write information
            for candle in candlestick_data:
                write_candlestick_row(candle, candlestick_writer)

        # Make remaining API calls
        if remaining_req_count > 0:
            url = f"https://api.upbit.com/v1/candles/{interval}?market={market}&count={remaining_req_count}&to={end_date.strftime('%Y-%m-%dT%H:%M:%S')}"
            response = requests.get(url, headers=headers)
            candlestick_data = response.json()
            end_date = end_date - datetime.timedelta(minutes=200)

            # Write information
            for candle in candlestick_data:
                write_candlestick_row(candle, candlestick_writer)

    print(f'Data written to {csv_filename}')

import pandas as pd

def past_kimpga(binance_csv, upbit_csv,symbol):
    output_csv = f"kimpga_history ({symbol}).csv"
    
    currency = get_currency("USD")

    binance_data = pd.read_csv(binance_csv)["Close price"]
    binance_krw = binance_data * currency
    upbit_data = pd.read_csv(upbit_csv)["Close price"]
    timestamp_data = pd.read_csv(upbit_csv)["Close time"]
    
    
    kimp_value = ((upbit_data / (binance_data * currency)) - 1) * 100
    inverse_kimp_value = (((binance_data * currency) / upbit_data) - 1) * 100
    
    result_df = pd.DataFrame({
        'timestamp': timestamp_data,
        'binance_close': binance_data,
        'binance_KRW':binance_krw,
        'upbit_close': upbit_data,
        'Kimp': kimp_value,
        'Inverse Kimp': inverse_kimp_value
    })
    

    result_df.to_csv(output_csv, index=False)

        

# # Test settings 
# balance = 1000
# symbol_upbit = 
# interval_binance = "1d"
# start_date = 
# end_date = 
# delay = 5  # in seconds


# Get price history from binance and upbit
# get_upbit_candlestick("XRP",  "minutes/1", "2021-05-07T00:00:00", "2022-05-21T00:00:00")
get_binance_candlestick_data("XRP", Client.KLINE_INTERVAL_1DAY, "07 May, 2021", "21 May, 2021")
# past_kimpga("binance_XRP.csv","upbit_XRP.csv","XRP")






