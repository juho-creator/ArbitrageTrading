import pandas as pd
from Layer1_API import kimpga
import time
import requests

# Initialize a dataframe to keep track of transactions
columns = ['timestamp', 'type', 'balance', 'crypto_value', 'gimp']
transactions_df = pd.DataFrame(columns=columns)

def record_transaction(timestamp, transaction_type, balance, crypto_value, gimp):
    global transactions_df
    transactions_df = transactions_df.append({
        'timestamp': timestamp,
        'type': transaction_type,
        'balance': balance,
        'crypto_value': crypto_value,
        'gimp': gimp
    }, ignore_index=True)

# Set initial balance and currency values
balance = 1000
currency = 1300
symbol = "BTC"

# Get initial price difference across exchanges
kimp, upbit, binance = kimpga(symbol)

# Record initial state
record_transaction(time.time(), 'initial', balance, balance * upbit, 0)

# If KIMP (Binance -> Upbit)
if kimp == "김프":
    # Refresh price
    binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    binance_response = requests.get(binance_url)
    binance = float(binance_response.json()["price"])

    # Buy at Binance
    balance -= binance * currency
    record_transaction(time.time(), 'buy', balance, balance * binance, 1)

    # Crypto transfer delay
    time.sleep(10)

    # Refresh price
    upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
    upbit_response = requests.get(upbit_url)
    upbit = float(upbit_response.json()[0]["trade_price"])

    # Sell at Upbit
    balance += upbit
    record_transaction(time.time(), 'sell', balance, balance * upbit, 1)

# If ReverseKIMP (Upbit -> Binance)
elif kimp == "역프":
    # Refresh price
    upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
    upbit_response = requests.get(upbit_url)
    upbit = float(upbit_response.json()[0]["trade_price"])

    # Buy at Upbit
    balance -= upbit
    record_transaction(time.time(), 'buy', balance, balance * upbit, 0)

    # Crypto transfer delay
    time.sleep(10)

    # Refresh price
    binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    binance_response = requests.get(binance_url)
    binance = float(binance_response.json()["price"])

    # Sell at Binance
    balance += binance * currency
    record_transaction(time.time(), 'sell', balance, balance * binance, 0)

# Save transactions to CSV
transactions_df.to_csv('transactions.csv', index=False)

print("Transactions recorded successfully.")
