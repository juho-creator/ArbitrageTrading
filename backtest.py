import pandas as pd
from Layer1_API import kimpga
import time
import requests

# Initialize a dataframe to keep track of transactions
columns = ['timestamp', 'gimp', 'exchange', 'type', 'crypto_price', 'balance']
transactions_df = pd.DataFrame(columns=columns)

# Define a function to record transactions in the dataframe
def record_transaction(timestamp, gimp, exchange, transaction_type, crypto_price, balance):
    global transactions_df
    transactions_df = transactions_df.append({
        'timestamp': timestamp,
        'gimp': gimp,
        'exchange': exchange,
        'type': transaction_type,
        'crypto_price': crypto_price,
        'balance': balance
    }, ignore_index=True)

# Set initial balance and currency values
balance = 1000
currency = 1300
symbol = "BTC"

# Get initial price difference across exchanges using the kimpga function
kimp, upbit, binance = kimpga(symbol)

# Record initial state
record_transaction(time.time(), 0, 'both', 'initial', upbit, balance)

# If KIMP (Binance -> Upbit)
if kimp == "김프":
    # Refresh price for Binance
    binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    binance_response = requests.get(binance_url)
    binance = float(binance_response.json()["price"])

    # Buy at Binance
    balance -= binance * currency
    record_transaction(time.time(), 1, 'Binance', 'buy', binance, balance)

    # Crypto transfer delay
    time.sleep(10)

    # Refresh price for Upbit
    upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
    upbit_response = requests.get(upbit_url)
    upbit = float(upbit_response.json()[0]["trade_price"])

    # Sell at Upbit
    balance += upbit
    record_transaction(time.time(), 1, 'Upbit', 'sell', upbit, balance)

# If ReverseKIMP (Upbit -> Binance)
elif kimp == "역프":
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
```

This modified structure should meet your column requirements. If you have any further adjustments or questions, feel free to let me know!Certainly, here's the modified code structure based on your requirements:

```python
import pandas as pd
from Layer1_API import kimpga
import time
import requests

# Initialize a dataframe to keep track of transactions
columns = ['timestamp', 'gimp', 'exchange', 'type', 'crypto_price', 'balance']
transactions_df = pd.DataFrame(columns=columns)

# Define a function to record transactions in the dataframe
def record_transaction(timestamp, gimp, exchange, transaction_type, crypto_price, balance):
    global transactions_df
    transactions_df = transactions_df.append({
        'timestamp': timestamp,
        'gimp': gimp,
        'exchange': exchange,
        'type': transaction_type,
        'crypto_price': crypto_price,
        'balance': balance
    }, ignore_index=True)

# Set initial balance and currency values
balance = 1000
currency = 1300
symbol = "BTC"

# Get initial price difference across exchanges using the kimpga function
kimp, upbit, binance = kimpga(symbol)

# Record initial state
record_transaction(time.time(), 0, 'both', 'initial', upbit, balance)

# If KIMP (Binance -> Upbit)
if kimp == "김프":
    # Refresh price for Binance
    binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    binance_response = requests.get(binance_url)
    binance = float(binance_response.json()["price"])

    # Buy at Binance
    balance -= binance * currency
    record_transaction(time.time(), 1, 'Binance', 'buy', binance, balance)

    # Crypto transfer delay
    time.sleep(10)

    # Refresh price for Upbit
    upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
    upbit_response = requests.get(upbit_url)
    upbit = float(upbit_response.json()[0]["trade_price"])

    # Sell at Upbit
    balance += upbit
    record_transaction(time.time(), 1, 'Upbit', 'sell', upbit, balance)

# If ReverseKIMP (Upbit -> Binance)
elif kimp == "역프":
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