import pandas as pd
from module import *
import time
import requests
import msvcrt
import datetime

# Initialize a dataframe to keep track of transactions
columns = ['timestamp', 'kimp', 'exchange', 'type', 'price', 'balance']
transactions_df = pd.DataFrame(columns=columns)



# Define a function to record transactions in the dataframe
def record_transaction(timestamp, kimp, exchange, transaction_type, crypto_price, balance):
    global transactions_df

    # Create a new DataFrame for the new row
    new_row = pd.DataFrame({
        'timestamp': [timestamp],
        'kimp': [kimp],
        'exchange': [exchange],
        'type': [transaction_type],
        'crypto_price': [crypto_price],
        'balance': [balance]
    })

    # Concatenate the new row DataFrame to the existing transactions_df
    transactions_df = pd.concat([transactions_df, new_row], ignore_index=True)


def forwardtest(balance, currency, symbol, delay,current_cash_location):
    # Get initial price difference across exchanges using the kimpga function
    print("__INITIAL STATE__")
    kimp, binance, upbit = current_kimpga(symbol,currency)
    
    # Record initial state
    record_transaction(datetime.datetime.now().strftime('%Y-%m-%d %X'), kimp, 'Initial', binance, upbit, balance)
    print(datetime.datetime.now().strftime('%Y-%m-%d %X'), kimp, 'Initial', round(binance*currency,2), round(upbit,2), balance)

    while(1):
        # Keep checking Kimp
        kimp, binance, upbit = current_kimpga(symbol,currency)
        print(datetime.datetime.now().strftime('%Y-%m-%d %X'), kimp, 'current', round(binance*currency,2), round(upbit,2), round(balance,2))


        # If KIMP (Binance -> Upbit)
        if kimp and current_cash_location == "binance":
            print("\n__KIMP TRANSACTION__")
            # Refresh price for Binance
            binance = binance_price(symbol)

            # Buy at Binance
            balance -= binance * currency
            record_transaction(datetime.datetime.now().strftime('%Y-%m-%d %X'), 1, 'Binance', 'buy', binance, balance)
            print(datetime.datetime.now().strftime('%Y-%m-%d %X'), 1, 'Binance', 'buy', round(binance*currency,2), round(balance,2))

            # Crypto transfer delay
            print(f"Transfering {symbol} (Binance -> Upbit)...")
            time.sleep(delay)

            # Refresh price for Upbit
            upbit = upbit_price(symbol)

            # Sell at Upbit
            balance += upbit
            record_transaction(datetime.datetime.now().strftime('%Y-%m-%d %X'), 1, 'Upbit', 'sell', upbit, balance)
            print(datetime.datetime.now().strftime('%Y-%m-%d %X'), 1, 'Upbit', 'sell', round(upbit,2), round(balance,2))

            # Update cash location 
            current_cash_location = "upbit"
            print(f"Cash deposited at {current_cash_location}")

        # If ReverseKIMP (Upbit -> Binance)
        elif not(kimp) and current_cash_location == "upbit":
            print("\n__INV KIMP TRANSACTION__")
            # Refresh price for Upbit
            upbit = upbit_price(symbol)


            # Buy at Upbit
            balance -= upbit
            record_transaction(datetime.datetime.now().strftime('%Y-%m-%d %X'), 0, 'Upbit', 'buy', round(upbit,2), round(balance,2))
            print(datetime.datetime.now().strftime('%Y-%m-%d %X'), 0, 'Upbit', 'buy', round(upbit,2), round(balance,2))

            # Crypto transfer delay
            print(f"Transfering {symbol} (Binance -> Upbit)...")
            time.sleep(10)

            # Refresh price for Binance
            binance = binance_price(symbol)


            # Sell at Binance
            balance += binance * currency
            record_transaction(datetime.datetime.now().strftime('%Y-%m-%d %X'), 0, 'Binance', 'sell', binance, balance)
            print(datetime.datetime.now().strftime('%Y-%m-%d %X'), 0, 'Binance', 'sell', round(binance * currency,2), round(balance,2))


            # Update cash location 
            current_cash_location = "binance"
            print(f"Cash deposited at {current_cash_location}")

        
        # Check for 'c' key press to break out of the loop
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'c':
                break


    print("Forward Testing paused")

    # Save transactions to CSV
    transactions_df.to_csv('transactions.csv', index=False)

    # Print success message
    print("Transactions recorded successfully.")





# ### Test Settings
# Set initial balance and currency values
current_cash_location = "binance"
balance = 10000
currency = get_currency("USD")
symbol = "XRP"
delay = 20


# Forward Test
import time
start_time = time.time()
forwardtest(balance, currency, symbol, delay, current_cash_location)
print("--- %s seconds ---" % (time.time() - start_time))
