from upbit_user import *
from binance.binance_user import *


# For Arbitrage Trading
def Reverse(symbol, transaction_fee):
    print("---REVERSE----")

    # Check KRW balance
    KRW = krw_balance()

    # Buy from UPBIT (Quantity : KRW)
    upbit_buy(symbol, KRW)

    # Check crypto quantity
    UPBIT_CRYPTO = crypto_balance(symbol)

    # Send to Binance (Quantity : XRP)
    UpbitWithDraw(symbol, UPBIT_CRYPTO)

    # Check crypto quantity (binance)
    BINANCE_CRYPTO = BinanceCRYPTO(symbol)

    # Sell at Binance (Quantity = XRP)
    BinanceSEll(symbol, BINANCE_CRYPTO)

def Kimp(symbol):
    print("---KIMP---")

    # Check USDT balance
    USDT = BinanceUSDT()

    # Buy at Binance (Quantity : USDT)
    BinanceBUY(symbol, USDT)

    # Check crypto quantity
    BINANCE_CRYPTO = BinanceCRYPTO(symbol)

    # Send to UPBIT (Quantity : XRP)
    TXID, quantity = BinanceWithDraw(symbol, BINANCE_CRYPTO)

    # Check if received from UPBIT
    UPBIT_CRYPTO = UpbitRECEIVED(TXID, symbol, quantity)

    # Sell from UPBIT (Quantity : XRP)
    upbit_sell(symbol, UPBIT_CRYPTO)




def TransferArbitrage():
    # Initializing parameters
    symbol = "EOS"
    reverse_percent = 2.8
    kimp_percent = 2

    # Get currency
    currency = get_currency_api("USD")

    exit_flag = False

    def signal_handler(signum, frame):
        nonlocal exit_flag
        exit_flag = True

    signal.signal(signal.SIGINT, signal_handler)

    while not exit_flag:
        start_time = time.time()

        kimp, binance, upbit = current_kimpga(symbol, currency)

        KRW = ()
        USDT = BinanceUSDT()

        Cash_at_upbit = KRW >= 6000
        Cash_at_binance = USDT >= 6

        if kimp <= reverse_percent and Cash_at_upbit:
            Reverse(symbol, 0)


        elif kimp >= kimp_percent and Cash_at_binance:
            Kimp(symbol)


        print("--- %s seconds ---" % (time.time() - start_time))

