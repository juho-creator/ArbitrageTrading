from arbitrage_trading import *
import time
import keyboard


### BETA CODE with single API call
# Triangular Arbitrage
def upbit_triangular(krw):
    
    # 1. Get all prices from orderbook 
    orderbook = get_orderbook_prices()
    available_btc_qty = krw / orderbook["KRW_BTC_ASK"]

    if available_btc_qty >= 0.0005:

        # 2. Compute available order quantity with current balance
        available_qty = get_available_qty(krw, orderbook)

        # Get new price
        new_prices = get_new_prices(orderbook)
        
        # 3. Print triangular Arbitrage status
        expected_profits = print_triangular_arbitrage(orderbook, available_qty, new_prices)

        # 4. Execute orders
        profit = execute_triangular_arbitrage(krw, orderbook, available_qty, new_prices, expected_profits)

        # # 5. Calculate Balance after trading
        # current_balance = balance_after_arbitrage(krw, profit)

        # return current_balance, profit
    else:
        print("Insufficient BTC")
        print(f"{available_btc_qty} < 0.0005 ({available_btc_qty < 0.0005})")
        
    # notify(f"Balance after trading :  ₩{current_balance}")


krw = 49000

# Set the duration to run the function (in seconds)
duration = 20 * 60  # 5 minutes

# Get the current time
start_time = time.time()


# Run the function for the specified duration
while time.time() - start_time < duration:
    start_time1= time.time()
    
    upbit_triangular(krw)
    print("--- %s seconds ---" % (time.time() - start_time1))


