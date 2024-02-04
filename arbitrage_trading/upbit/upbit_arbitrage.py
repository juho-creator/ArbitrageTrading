import requests
from .upbit_user import *

# Cryptos supporting triangular arbitrage
available_cryptos = [
    "AHT",
    "META",
    "JST",
    "BSV",
    "CTC",
    "WAVES",
    "SEI",
    "MED",
    "LOOM",
    "CELO",
    "ETC",
    "MASK",
    "BLUR",
    "SOL",
    "AQT",
    "STORJ",
    "TRX",
    "GRT",
    "ASTR",
    "STRK",
    "DKA",
    "CRO",
    "XTZ",
    "IQ",
    "T",
    "IOST",
    "BCH",
    "ANKR",
    "ETH",
    "ARB",
    "SBD",
    "CHZ",
    "MANA",
    "SUI",
    "SXP",
    "AXS",
    "EGLD",
    "LSK",
    "HUNT",
    "FCT2",
    "MOC",
    "ZRX",
    "HPO",
    "AERGO",
    "LINK",
    "STMX",
    "STPT",
    "STRAX",
    "STX",
    "PLA",
    "UPP",
    "ARK",
    "XLM",
    "HIFI",
    "MVL",
    "MLK",
    "ZIL",
    "EOS",
    "SAND",
    "IMX",
    "KAVA",
    "ORBS",
    "TON",
    "CBK",
    "HIVE",
    "1INCH",
    "DOT",
    "GLM",
    "POWR",
    "XRP",
    "BORA",
    "GMT",
    "SC",
    "DOGE",
    "VET",
    "MTL",
    "PUNDIX",
    "BAT",
    "ATOM",
    "XEM",
    "MATIC",
    "ADA",
    "AAVE",
    "GRS",
    "AVAX",
    "FLOW",
    "APT",
    "SNT",
    "STEEM",
    "SSX",
    "MINA",
    "NEAR",
    "POLYX",
    "ALGO",
    "QTUM",
    "CVC",
    "ELF",
    "ARDR",
    "WAXP",
]



# Directions
def oneway_market(symbol,KRW):
    # Market Orders
    crypto = upbit_buy(f"KRW-{symbol}", KRW)
    upbit_sell(f"BTC-{symbol}", crypto)
    BTC = crypto_balance("BTC")
    upbit_sell(f"KRW-BTC", BTC)

def oneway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, KRW):
        volume = KRW / KRW_CODE
        CODE_QTY = upbit_limit_buy(f"KRW-{symbol}", KRW_CODE, volume)
        print(CODE_QTY)
        CODE_QTY = upbit_limit_sell(f"BTC-{symbol}", BTC_CODE, CODE_QTY) 
        BTC_QTY = CODE_QTY * BTC_CODE * 0.9975
        print(BTC_QTY)
        upbit_limit_sell(f"KRW-BTC", KRW_BTC, BTC_QTY)

def one_way(symbol, KRW_CODE="", BTC_CODE="", KRW_BTC="", order_type="limit"):
    KRW = krw_balance()
    try:
        if order_type == "market":
            oneway_market(symbol, KRW)
        
        elif order_type == "limit":
            oneway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, KRW)
    except:
        pass

def otherway_market(symbol,KRW):
    BTC = upbit_buy(f"KRW-BTC", KRW)
    BTC = BTC * 0.9975
    crypto = upbit_buy(f"BTC-{symbol}", BTC)
    upbit_sell(f"KRW-{symbol}", crypto)

def otherway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, KRW):
    BTC_QTY = KRW / KRW_BTC
    upbit_limit_buy(f"KRW-BTC", KRW_BTC, BTC_QTY)
    CODE_QTY = BTC_QTY / BTC_CODE * 0.9975    
    print(CODE_QTY)
    upbit_limit_buy(f"BTC-{symbol}", BTC_CODE, CODE_QTY)
    upbit_limit_sell(f"KRW-{symbol}", KRW_CODE, CODE_QTY)

def other_way(symbol, KRW_CODE="", BTC_CODE="", KRW_BTC="",order_type="limit"):
    KRW = krw_balance()
    try:
        if order_type == "market":
            otherway_market(symbol,KRW)
        elif order_type == "limit":
            otherway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, KRW)
    except:
        pass

#  Looking for Arbitrage opportunities :D
def get_orderbook_prices(code):
    url = f"https://api.upbit.com/v1/orderbook?markets=KRW-{code},BTC-{code},KRW-BTC"
    response = requests.get(url)
    data = response.json()

    KRW_CODE_ASK = data[0]["orderbook_units"][0]["ask_price"]
    KRW_CODE_BID = data[0]["orderbook_units"][0]["bid_price"]
    
    BTC_CODE_ASK  = data[1]["orderbook_units"][0]["ask_price"]
    BTC_CODE_BID  = data[1]["orderbook_units"][0]["bid_price"]
    
    KRW_BTC_ASK = data[2]["orderbook_units"][0]["ask_price"]
    KRW_BTC_BID = data[2]["orderbook_units"][0]["bid_price"]

    return KRW_CODE_ASK, KRW_CODE_BID, BTC_CODE_ASK, BTC_CODE_BID, KRW_BTC_ASK, KRW_BTC_BID

def find_direction_and_execute(code, KRW_CODE_ASK, KRW_CODE_BID, BTC_CODE_ASK, BTC_CODE_BID, KRW_BTC_ASK, KRW_BTC_BID):
    # Checking Oneway 
    NEW_KRW_CODE = round(BTC_CODE_BID * KRW_BTC_ASK,2)
    if KRW_CODE_BID < NEW_KRW_CODE:
        print("one_way(@)")
        print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")

        profit = round((NEW_KRW_CODE - KRW_CODE_BID) / KRW_CODE_BID * 100, 2)
        print(f"{KRW_CODE_BID} ==> {NEW_KRW_CODE} ({profit}%)")
        one_way(code, KRW_CODE_BID, BTC_CODE_BID, KRW_BTC_ASK, "limit")
        return
    
    # Checking Otherway
    NEW_KRW_BTC = round(KRW_CODE_ASK / BTC_CODE_ASK,2)
    if KRW_BTC_BID < NEW_KRW_BTC:
        print("other_way(@)")
        print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
        profit = round((NEW_KRW_BTC - KRW_BTC_BID) / KRW_BTC_BID * 100,2)
        print(f"{KRW_BTC_BID} ==> {NEW_KRW_BTC} ({profit}%)")
        other_way(code, KRW_BTC_BID, BTC_CODE_ASK, KRW_CODE_ASK, "limit")

        return
    else:
        print("one_way")
        print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")
        profit = round((NEW_KRW_CODE-KRW_CODE_BID)/KRW_CODE_BID*100,2)
        print(f"{KRW_CODE_BID} ==> {BTC_CODE_BID} * {KRW_BTC_ASK} = {NEW_KRW_CODE} ({profit}%)\n\n")
        
        print("other_way")
        print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
        profit = round((NEW_KRW_BTC - KRW_BTC_BID) / KRW_BTC_BID * 100,2)
        print(f"{KRW_BTC_BID} ==> {KRW_CODE_ASK} / {BTC_CODE_ASK} = {NEW_KRW_BTC} ({profit}%)\n\n")


# Triangular Arbitrage
def upbit_triangular(code):
    # Get prices from orderbook 
    KRW_CODE_ASK, KRW_CODE_BID, BTC_CODE_ASK, BTC_CODE_BID, KRW_BTC_ASK, KRW_BTC_BID = get_orderbook_prices(code)


    # Determine Arbitrage direction and exeecute orders
    find_direction_and_execute(code, KRW_CODE_ASK, KRW_CODE_BID, BTC_CODE_ASK, BTC_CODE_BID, KRW_BTC_ASK, KRW_BTC_BID)







# For Arbitrage Trading
def Reverse(symbol, transaction_fee):
    print("---REVERSE----")

    # Check KRW balance
    KRW = UpbitKRW()

    # Buy from UPBIT (Quantity : KRW)
    UpbitBUY(symbol, KRW)

    # Check crypto quantity
    UPBIT_CRYPTO = UpbitCRYPTO(symbol)

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
    UpbitSELL(symbol, UPBIT_CRYPTO)
            
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

        KRW = UpbitKRW()
        USDT = BinanceUSDT()

        Cash_at_upbit = KRW >= 6000
        Cash_at_binance = USDT >= 6

        if kimp <= reverse_percent and Cash_at_upbit:
            Reverse(symbol, 0)


        elif kimp >= kimp_percent and Cash_at_binance:
            Kimp(symbol)


        print("--- %s seconds ---" % (time.time() - start_time))





