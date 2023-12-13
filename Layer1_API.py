import requests

def kimpga(symbol):
    try:
        # Fetch Binance price
        binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        binance_response = requests.get(binance_url)
        binance_data = binance_response.json()
        binance_close = float(binance_data["price"])
        print(f"Current price of {symbol} on Binance: {binance_close}")

        # Fetch Upbit price
        upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
        upbit_response = requests.get(upbit_url)
        upbit_data = upbit_response.json()

        if len(upbit_data) > 0:
            upbit_close = float(upbit_data[0]["trade_price"])
            print(f"Current price of {symbol} on Upbit: {upbit_close}")
        else:
            print(f"No data received for {symbol} on Upbit.")
            upbit_close = None

        # Calculate the specified formula
        currency = 1319.4  # Replace with the actual currency value
        if upbit_close is not None and binance_close is not None:
            calculated_value = ((upbit_close / (binance_close * currency)) - 1) * 100
            print(f"Calculated Value for {symbol}: {calculated_value}")
            
            # Check if calculated value is greater than 0
            if calculated_value > 0:
                return "김프"
            else:
                return "역프"
        else:
            print(f"Failed to calculate for {symbol}. Check data fetching.")
            return None
    
    except Exception as e:
        print(f"Error in fetching data: {e}")
        return None


