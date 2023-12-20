import requests
from bs4 import BeautifulSoup

def get_currency(currency_code):
    url = f'https://m.stock.naver.com/marketindex/exchange/FX_{currency_code}KRW'
    headers = {'Accept-Language': 'ko-KR', 'User-Agent': 'Mozilla/5.0'}

    # HTTP request & response from Naver
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parsing HTML response data with lxml for better performance
        soup = BeautifulSoup(response.content, 'lxml')

        # Extract exchange rate using a more specific selector
        exchange_rate_tag = soup.select_one('strong.DetailInfo_price__I_VJn')

        # Check if the tag is found
        if exchange_rate_tag:
            # Extract text from the tag and clean it up
            exchange_rate = exchange_rate_tag.get_text(strip=True).replace("KRW", "").replace(",", "")

            try:
                # Convert the cleaned-up string to a float
                exchange_rate = float(exchange_rate)
                print(f"{currency_code}KRW = {exchange_rate}")
                return exchange_rate
            except ValueError:
                print("Failed to convert exchange rate to float.")
        else:
            print("Exchange rate tag not found.")
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")


def kimpga(symbol,currency):
    try:
        # Fetch Binance price
        binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        binance_response = requests.get(binance_url)
        binance_data = binance_response.json()
        binance_close = float(binance_data["price"])
        
        # Error Handling (Binance)
        if binance_close is not None:
            print(f"{symbol} price on Binance: $ {binance_close} (₩ {round(binance_close*currency,2)})")
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
            print(f"{symbol} price on Upbit: ₩ {upbit_close}")
        else:
            print(f"No data received for {symbol} on Upbit.")
            upbit_close = None

        # Calculate Kimp
        if upbit_close is not None and binance_close is not None:
            calculated_value = ((upbit_close / (binance_close * currency)) - 1) * 100
            print(f"Kimp {symbol}: {round(calculated_value, 2)} %")
            
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

# def main():
#     kimp, binance, upbit = kimpga("XRP")
#     print(kimp, binance, upbit)

# import time
# start_time = time.time()
# main()
# print("--- %s seconds ---" % (time.time() - start_time))
