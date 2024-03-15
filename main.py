from arbitrage_trading import *
import time


### BETA CODE with single API call
# Triangular Arbitrage
def upbit_triangular(krw):
    
    # 1. Get all prices from orderbook 
    orderbook = get_orderbook_prices()
    available_btc_qty = krw / orderbook["KRW_BTC_ASK"]

    if available_btc_qty >= 0.0005:

        for crypto in cryptos:
            # 2. Compute available order quantity with current balance
            available_qty = get_available_qty(crypto, krw, orderbook)

            # 3. Get new price
            new_prices = get_new_prices(crypto, orderbook)
            
            # 4. Print triangular Arbitrage status
            expected_profits = get_expected_profit(crypto, orderbook, new_prices)

            # 5. Execute orders
            execute_triangular_arbitrage(crypto, krw, orderbook, available_qty, new_prices, expected_profits)

        # # 5. Calculate Balance after trading
        # current_balance = balance_after_arbitrage(krw, profit)

        # return current_balance, profit
    else:
        print("Insufficient BTC")
        print(f"{available_btc_qty} < 0.0005 ({available_btc_qty < 0.0005})")
        
    # notify(f"Balance after trading :  ₩{current_balance}")


krw = 55000

#  Set the duration to run the function (in seconds)
duration = 10 * 60  # 5 minutes

start_time = time.time()

# Run the function for the specified duration
while(time.time() - start_time < duration): 
    test_start = time.time()
    upbit_triangular(krw)
    test_end = time.time()
    print("--- %s seconds ---" % (test_end - test_start))

