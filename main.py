from arbitrage_trading import *
import time
import keyboard


# Triangular Arbitrage
def upbit_triangular(code, krw):
    # 1. Get prices from orderbook 
    orderbook = get_orderbook_prices(code)

    # 2. Compute available order quantity with current balance
    available_qty = get_available_qty(krw, orderbook)

    # Get new price
    new_prices = get_new_prices(orderbook)
    
    # 3. Print triangular Arbitrage status
    expected_profits = print_triangular_arbitrage(code, orderbook, available_qty, new_prices)

    # 4. Execute orders
    profit = execute_triangular_arbitrage(code, orderbook, available_qty, new_prices, expected_profits)

    # 5. Calculate Balance after trading
    current_balance = balance_after_arbitrage(krw, profit)

    return current_balance, profit






# Testing with virtual money
def upbit_triangular_roundtrip(krw, count):
    start_time = time.time()
    # notify(f"Starting arbitrage detesction {count}")
    print(f"Starting arbitrage detection {count}")
    cryptos = available_cryptos
    for crypto in cryptos:
        if keyboard.is_pressed("a"):
            raise SystemExit

        print(f"\n\n{crypto}")
        krw, profit = upbit_triangular(crypto, krw)
    # notify("Arbitrage detection completed")
    if profit != 0:
        # notify(f"Balance after trading : {krw}")
        print(f"$ Balance after trading : {krw}")
    print("--- %s seconds ---" % (time.time() - start_time))
    return krw

def run_triangular_roundtrip(hour, initial_balance):
    seconds = hour * 3600
    krw = initial_balance
    count = 1

    start_time = time.time()
    while time.time() - start_time < seconds:
        krw = upbit_triangular_roundtrip(krw, count)
        count += 1 
    notify("Triangular Arbitrage Trading completed")


initial_balance = krw_balance()

# run_triangular_roundtrip(1, initial_balance)


krw, profit = upbit_triangular("CBK", initial_balance)
