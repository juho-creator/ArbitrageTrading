from ..config import *
import ccxt


api_params = {
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "enableRateLimit": True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    "options": {
        "adjustForTimeDifference": True,
    },
}

binance = ccxt.binance(
    {**api_params, "options": {"defaultType": "spot", "adjustForTimeDifference": True}}
)
binance_futures = ccxt.binance(
    {
        **api_params,
        "options": {"defaultType": "future", "adjustForTimeDifference": True},
    }
)

# TESTNET API setup
binance_futures_test = ccxt.binance(
    {
        "apiKey": TEST_KEY,
        "secret": TEST_SECRET,
        "enableRateLimit": True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
        "options": {
            "defaultType": "future",
            "adjustForTimeDifference": True,
        },
    }
)
binance_futures_test.set_sandbox_mode(True)  # comment if you're not using the testnet




# Placing Order
def BinanceBUY(symbol, USDT):
    print(f"\nBuying {symbol} at Binance")
    try:
        buy_binance = binance.create_market_buy_order(f"{symbol}USDT", USDT)

        order_id = buy_binance["info"]["orderId"]
        order_status = binance.fetchOrder(order_id, symbol + "USDT")["status"]
        while order_status != "closed":
            print(f"Buying {symbol} from Binance...")
            order_status = binance.fetchOrder(order_id, symbol + "USDT")["status"]
        print(f"Bought {symbol} from Binance")
    except:
        print("ORDER FAILED : Total order value should be more than 5 USDT")

def BinanceSEll(symbol, CRYPTO_AVAILABLE):
    print(f"Selling {symbol} at Binance")
    try:
        print(binance.create_market_sell_order(f"{symbol}USDT", CRYPTO_AVAILABLE))
    except:
        print("ORDER FAILED : Total order value should be more than 5 USDT")

# Checking balance
def BinanceUSDT():
    try:
        USDT = binance.fetch_balance()["free"]["USDT"]
        print(f"USDT balance : {USDT}")
        return USDT
    except Exception as e:
        print(e)
        raise SystemExit("IP  not registered in binance")

def BinanceCRYPTO(symbol):
    try:
        crypto_quantity = binance.fetch_balance()["free"][symbol]
        binance_quantity = "{:.6f}".format(crypto_quantity)
        print(f"\n{symbol} balance : {binance_quantity} (Binance)")
        return float(binance_quantity)
    except:
        print(f"Unable to retrieve {symbol} balance (Binance)")


# Withdrawal
def BinanceAddress(symbol):
    try:
        address = binance.fetchDepositAddress(symbol)["address"]
        tag = binance.fetchDepositAddress(symbol)["tag"]
        return address, tag
    except:
        print(f"{symbol} wallet not found")

def BinanceWithDraw(symbol, CRYPTO_AVAILABLE):
    try:
        address, tag = UpbitAddress(symbol)

        withdrawal = binance.withdraw(
            symbol, CRYPTO_AVAILABLE, address, tag, {f"chain": {symbol}}
        )
        print(f"\nWithdrawing {symbol} (Binance -> UPBIT)")
        print(withdrawal)

        TXID = None
        while TXID == None:
            print(f"Transfering {symbol} (Binance -> UPBIT)")
            withdraw = binance.fetchWithdrawals(symbol, limit=1)
            pprint(withdraw)
            TXID = withdraw[0]["txid"]
            quantity = withdraw[0]["amount"]
        print("Successfully sent to UPBIT")
        return TXID, quantity
    except:
        print(f"Unable to withdraw {symbol} from Binance")






