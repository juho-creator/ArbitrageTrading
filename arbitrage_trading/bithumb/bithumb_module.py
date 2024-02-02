def bithumb_price(symbol):
    try:
        url = f"https://api.bithumb.com/public/ticker/{symbol}"

        response = requests.get(url).text
        data = json.loads(response)
        return float(data["data"]["prev_closing_price"])
    except:
        print(f"Unable to get {symbol} price")



# OKX
# Bybit
# Binance
# BitMEX
# Bitget
# Crypto.com
# HTX


