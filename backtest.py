import requests
import csv

def get_upbit_candlestick(symbol,start_date, end_date):
    market = f"KRW-{symbol}"
    interval = "minutes/1"
    count = 1000  # Adjust count based on your requirements
    url = f"https://api.upbit.com/v1/candles/{interval}?market={market}&count={count}&from={start_date}T00:00:00Z&to={end_date}T23:59:59Z"
    
    headers = {"accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    candlestick_data = response.json()

    # Open CSV File
    csvfile = open('upbit_candlestick_data.csv', 'w', newline='')
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

# Example usage:
# get_upbit_candlestick("XRP",2023-01-01", "2023-12-31")
