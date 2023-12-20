import pandas as pd
from Layer1_API import kimpga,get_currency
import time
import requests

# Initialize a dataframe to keep track of transactions
columns = ['timestamp', 'kimp', 'exchange', 'type', 'crypto_price', 'balance']
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


def forwardtest(balance, currency, symbol, delay):
    # Get initial price difference across exchanges using the kimpga function
    kimp, binance, upbit = kimpga(symbol,currency)
    
    # Record initial state
    record_transaction(time.time(), kimp, 'Initial', binance, upbit, balance)

    # If KIMP (Binance -> Upbit)
    if kimp:
        # Refresh price for Binance
        binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        binance_response = requests.get(binance_url)
        binance = float(binance_response.json()["price"])

        # Buy at Binance
        balance -= binance * currency
        record_transaction(time.time(), 1, 'Binance', 'buy', binance, balance)

        # Crypto transfer delay
        time.sleep(delay)

        # Refresh price for Upbit
        upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
        upbit_response = requests.get(upbit_url)
        upbit = float(upbit_response.json()[0]["trade_price"])

        # Sell at Upbit
        balance += upbit
        record_transaction(time.time(), 1, 'Upbit', 'sell', upbit, balance)

    # If ReverseKIMP (Upbit -> Binance)
    elif not(kimp):
        # Refresh price for Upbit
        upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
        upbit_response = requests.get(upbit_url)
        upbit = float(upbit_response.json()[0]["trade_price"])

        # Buy at Upbit
        balance -= upbit
        record_transaction(time.time(), 0, 'Upbit', 'buy', upbit, balance)

        # Crypto transfer delay
        time.sleep(10)

        # Refresh price for Binance
        binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        binance_response = requests.get(binance_url)
        binance = float(binance_response.json()["price"])

        # Sell at Binance
        balance += binance * currency
        record_transaction(time.time(), 0, 'Binance', 'sell', binance, balance)

    # Save transactions to CSV
    transactions_df.to_csv('transactions.csv', index=False)

    # Print success message
    print("Transactions recorded successfully.")

# Set initial balance and currency values
balance = 1000
currency = get_currency("USD")
symbol = "XRP"
delay = 20






import time
start_time = time.time()
forwardtest(balance, currency, symbol, delay)
print("--- %s seconds ---" % (time.time() - start_time))
