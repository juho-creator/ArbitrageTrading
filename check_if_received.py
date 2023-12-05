def check_if_received(symbol,exchange):
    if  API_REQUEST == crypto_received:
        return 1
    return 0
    

received = 0

while not received:
    received = check_if_received('XRP','Binance')

