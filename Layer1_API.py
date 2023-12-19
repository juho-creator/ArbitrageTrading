import requests

def kimpga(symbol):
    # Initialize currency
    currency = 1300.00  

    try:
        # Fetch Binance price
        binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        binance_response = requests.get(binance_url)
        binance_data = binance_response.json()
        binance_close = float(binance_data["price"])
        
        # Error Handling (Binance)
        if binance_close is not None:
            print(f"Current price of {symbol} on Binance: $ {binance_close}")
        else:
            print(f"No data received for {symbol} on Binance.")
            binance_close = None

        # Fetch Upbit price
        upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
        upbit_response = requests.get(upbit_url)
        upbit_data = upbit_response.json()

        # Error Handling (Upbit)
        if len(upbit_data) > 0:
            upbit_close = float(upbit_data[0]["trade_price"])
            print(f"Current price of {symbol} on Upbit: ₩ {upbit_close}")
        else:
            print(f"No data received for {symbol} on Upbit.")
            upbit_close = None

        # Calculate Kimp
        if upbit_close is not None and binance_close is not None:
            calculated_value = ((upbit_close / (binance_close * currency)) - 1) * 100
            print(f"Calculated Value for {symbol}: {round(calculated_value, 2)}")
            
            if calculated_value > 0:
                return 1, binance_close, upbit_close  # 김프
            else:
                return 0, binance_close, upbit_close  # 역프
        
        else:
            print(f"Failed to calculate for {symbol}. Check data fetching.")
            return None
    
    except Exception as e:
        print(f"Error in fetching data: {e}")
        return None


kimp, binance, upbit = kimpga("XRP")

print(kimp, binance, upbit)
