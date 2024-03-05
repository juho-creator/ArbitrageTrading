import requests
from .upbit_user import *
from gtts import gTTS
from playsound import playsound
import os 
from .upbit_module import *

def notify(mytext):
    myobj = gTTS(text=mytext, lang="en", slow=False)
    myobj.save("test.mp3")
    playsound("test.mp3")
    os.remove("test.mp3")




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
    
    orderbook = {}
    orderbook["KRW_CODE_ASK"] = data[0]["orderbook_units"][0]["ask_price"]
    orderbook["KRW_CODE_BID"] = data[0]["orderbook_units"][0]["bid_price"]
    orderbook["KRW_CODE_BIDSIZE"] = data[0]["orderbook_units"][0]["bid_size"]

    orderbook["BTC_CODE_ASK"]  = data[1]["orderbook_units"][0]["ask_price"]
    orderbook["BTC_CODE_BID"]  = data[1]["orderbook_units"][0]["bid_price"]
    
    orderbook["BTC_CODE_ASKSIZE"]  = data[1]["orderbook_units"][0]["ask_size"]
    orderbook["BTC_CODE_BIDSIZE"]  = data[1]["orderbook_units"][0]["bid_size"]
    
    
    orderbook["KRW_BTC_ASK"] = data[2]["orderbook_units"][0]["ask_price"]
    orderbook["KRW_BTC_BID"] = data[2]["orderbook_units"][0]["bid_price"]
    orderbook["KRW_BTC_BIDSIZE"] = data[2]["orderbook_units"][0]["bid_size"]
    
    return orderbook

def print_oneway(code, orderbook, NEW_KRW_CODE, oneway_qty):
    print("one_way")
    print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")
    oneway_profit = round((NEW_KRW_CODE - orderbook["KRW_CODE_ASK"]) / orderbook["KRW_CODE_ASK"] * 100, 2)
    if oneway_profit > 0:
        print(f"{orderbook["KRW_CODE_ASK"]} ==> {NEW_KRW_CODE} (+{oneway_profit}%)")
    else:
        print(f"{orderbook["KRW_CODE_ASK"]} ==> {NEW_KRW_CODE} ({oneway_profit}%)")

    print(f"BTC_CODE qty : { orderbook["BTC_CODE_BIDSIZE"]} >= {oneway_qty["code_qty"]} ({orderbook["BTC_CODE_BIDSIZE"] >= oneway_qty["code_qty"]})")
    print(f"KRW_BTC qty : {orderbook["KRW_BTC_BIDSIZE"]} >= {oneway_qty["btc_qty"]} ({orderbook["KRW_BTC_BIDSIZE"] >= oneway_qty["btc_qty"]})")
    print(f"profit : {oneway_profit} > 0.35 ({oneway_profit > 0.35})\n")

    return oneway_profit

def print_otherway(code, orderbook, NEW_KRW_BTC, otherway_qty):
    print("\nother_way")
    print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
    otherway_profit = round((NEW_KRW_BTC - orderbook["KRW_BTC_ASK"]) / orderbook["KRW_BTC_ASK"] * 100,2)
    if otherway_profit > 0:
        print(f"{orderbook["KRW_BTC_ASK"]} ==> {NEW_KRW_BTC} (+{otherway_profit}%)")
    else:
        print(f"{orderbook["KRW_BTC_ASK"]} ==> {NEW_KRW_BTC} ({otherway_profit}%)")
    print(f"BTC_CODE qty : {orderbook["BTC_CODE_ASKSIZE"]} > {otherway_qty["code_qty"]} ({orderbook["BTC_CODE_ASKSIZE"] > otherway_qty["code_qty"]})")
    print(f"KRW_CODE qty : {orderbook["KRW_CODE_BIDSIZE"]} > {otherway_qty["code_qty"]} ({orderbook["KRW_CODE_BIDSIZE"] > otherway_qty["code_qty"]})")
    print(f"profit : {otherway_profit} > 0.35 ({otherway_profit > 0.35})\n")

    return otherway_profit

def print_triangular_arbitrage(code, orderbook, available_qty, new_prices):
    expected_profits = {}
    expected_profits["oneway_profit"] = print_oneway(code, orderbook, new_prices["NEW_KRW_CODE"], available_qty["oneway"])
    expected_profits["otherway_profit"] = print_otherway(code, orderbook, new_prices["NEW_KRW_BTC"], available_qty["otherway"])

    return expected_profits

def execute_triangular_arbitrage(code, orderbook, available_qty, new_prices, expected_profits):
    # Checking Oneway 
    if (orderbook["KRW_CODE_BID"] < new_prices["NEW_KRW_CODE"])  and (orderbook["BTC_CODE_BID"] * orderbook["BTC_CODE_BIDSIZE"] >= available_qty["oneway_btc_qty"]) and  (orderbook["KRW_BTC_BIDSIZE"] >= available_qty["oneway_btc_qty"]) and (expected_profits["oneway_profit"] > 0.35):
        one_way(code, orderbook["KRW_CODE_ASK"], orderbook["BTC_CODE_BID"], orderbook["KRW_BTC_BID"], "limit")
        notify("oneway order executed")
        print(f"@ ONEWAY ORDER EXECUTED : {code}")
        return expected_profits["oneway_profit"]
    
    # Checking Otherway
    elif (orderbook["KRW_BTC_ASK"] < new_prices["NEW_KRW_BTC"]) and  (orderbook["BTC_CODE_ASKSIZE"] > available_qty["otherway_code_qty"]) and (orderbook["KRW_CODE_BIDSIZE"] > available_qty["otherway_code_qty"]) and (expected_profits["otherway_profit"] > 0.35):
        other_way(code, orderbook["KRW_CODE_BID"], orderbook["BTC_CODE_ASK"], orderbook["KRW_BTC_ASK"], "limit")
        notify("otherway order executed")
        print(f"@ OTHERWAY ORDER EXECUTED : {code}")
        return expected_profits["otherway_profit"]
    
    return 0


def get_available_qty(krw, orderbook):
    available_qty = {
        "oneway": {},
        "otherway": {}
    }
    available_qty["oneway"]["code_qty"] = krw / orderbook["KRW_CODE_ASK"]
    available_qty["oneway"]["btc_qty"] = available_qty["oneway"]["code_qty"] * orderbook["BTC_CODE_BID"]

    available_qty["otherway"]["code_qty"] = (krw / orderbook["KRW_BTC_ASK"]) / orderbook["BTC_CODE_ASK"]

    return available_qty


def get_new_prices(orderbook):
    new_prices = {}
    
    new_prices["NEW_KRW_CODE"] = round(orderbook["BTC_CODE_BID"] * orderbook["KRW_BTC_BID"],2)
    new_prices["NEW_KRW_BTC"] = round(orderbook["KRW_CODE_BID"] / orderbook["BTC_CODE_ASK"],2)

    return new_prices


def balance_after_arbitrage(krw, profit):
    if profit != 0:
        krw = krw * (1 + profit / 100) * 0.9965
    return krw








