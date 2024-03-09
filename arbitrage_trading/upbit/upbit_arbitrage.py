import requests
from .upbit_user import *
from .upbit_module import *




# Cryptos supporting triangular arbitrage
cryptos = [
    "ETH", "MTL", "XRP", "ETC", "SNT", "WAVES", "XEM", "QTUM", "LSK", "STEEM",
    "XLM", "ARDR", "ARK", "STORJ", "GRS", "ADA", "SBD", "POWR", "EOS", "TRX",
    "SC", "ZIL", "POLYX", "ZRX", "LOOM", "BCH", "BAT", "IOST", "CVC", "IQ",
    "HIFI", "UPP", "ELF", "BSV", "MOC", "MANA", "ANKR", "AERGO", "ATOM", "WAXP",
    "MED", "MLK", "STPT", "ORBS", "VET", "CHZ", "STMX", "DKA", "HIVE", "KAVA",
    "AHT", "LINK", "XTZ", "BORA", "JST", "CRO", "TON", "SXP", "HUNT", "PDA",
    "DOT", "MVL", "STRAX", "AQT", "GLM", "SSX", "META", "FCT2", "CBK", "SAND",
    "HPO", "DOGE", "STRIKE", "PUNDIX", "FLOW", "AXS", "STX", "SOL", "MATIC",
    "AAVE", "1INCH", "ALGO", "NEAR", "AVAX", "T", "CELO", "GMT", "APT", "MASK",
    "ARB", "EGLD", "SUI", "GRT", "BLUR", "IMX", "SEI", "MINA", "CTC", "ASTR",
    "ID", "PYTH"
]



# Directions
def oneway_market(symbol,KRW):
    # Market Orders
    crypto = upbit_buy(f"KRW-{symbol}", KRW)
    upbit_sell(f"BTC-{symbol}", crypto)
    BTC = crypto_balance("BTC")
    upbit_sell(f"KRW-BTC", BTC)

def oneway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, krw):
        volume = krw / KRW_CODE
        CODE_QTY = upbit_limit_buy(f"KRW-{symbol}", KRW_CODE, volume)
        CODE_QTY = upbit_limit_sell(f"BTC-{symbol}", BTC_CODE, CODE_QTY) 
        BTC_QTY = CODE_QTY * BTC_CODE * 0.9975
        upbit_limit_sell(f"KRW-BTC", KRW_BTC, BTC_QTY)

def one_way(symbol, krw, KRW_CODE="", BTC_CODE="", KRW_BTC="", order_type="limit"):

    try:
        if order_type == "market":
            oneway_market(symbol, krw)
        
        elif order_type == "limit":
            oneway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, krw)
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
def get_orderbook_prices():
    url = f"https://api.upbit.com/v1/orderbook?markets=KRW-BTC,KRW-ETH,BTC-ETH,KRW-MTL,BTC-MTL,KRW-XRP,BTC-XRP,KRW-ETC,BTC-ETC,KRW-SNT,BTC-SNT,KRW-WAVES,BTC-WAVES,KRW-XEM,BTC-XEM,KRW-QTUM,BTC-QTUM,KRW-LSK,BTC-LSK,KRW-STEEM,BTC-STEEM,KRW-XLM,BTC-XLM,KRW-ARDR,BTC-ARDR,KRW-ARK,BTC-ARK,KRW-STORJ,BTC-STORJ,KRW-GRS,BTC-GRS,KRW-ADA,BTC-ADA,KRW-SBD,BTC-SBD,KRW-POWR,BTC-POWR,KRW-EOS,BTC-EOS,KRW-TRX,BTC-TRX,KRW-SC,BTC-SC,KRW-ZIL,BTC-ZIL,KRW-POLYX,BTC-POLYX,KRW-ZRX,BTC-ZRX,KRW-LOOM,BTC-LOOM,KRW-BCH,BTC-BCH,KRW-BAT,BTC-BAT,KRW-IOST,BTC-IOST,KRW-CVC,BTC-CVC,KRW-IQ,BTC-IQ,KRW-HIFI,BTC-HIFI,KRW-UPP,BTC-UPP,KRW-ELF,BTC-ELF,KRW-BSV,BTC-BSV,KRW-MOC,BTC-MOC,KRW-MANA,BTC-MANA,KRW-ANKR,BTC-ANKR,KRW-AERGO,BTC-AERGO,KRW-ATOM,BTC-ATOM,KRW-WAXP,BTC-WAXP,KRW-MED,BTC-MED,KRW-MLK,BTC-MLK,KRW-STPT,BTC-STPT,KRW-ORBS,BTC-ORBS,KRW-VET,BTC-VET,KRW-CHZ,BTC-CHZ,KRW-STMX,BTC-STMX,KRW-DKA,BTC-DKA,KRW-HIVE,BTC-HIVE,KRW-KAVA,BTC-KAVA,KRW-AHT,BTC-AHT,KRW-LINK,BTC-LINK,KRW-XTZ,BTC-XTZ,KRW-BORA,BTC-BORA,KRW-JST,BTC-JST,KRW-CRO,BTC-CRO,KRW-TON,BTC-TON,KRW-SXP,BTC-SXP,KRW-HUNT,BTC-HUNT,KRW-PDA,BTC-PDA,KRW-DOT,BTC-DOT,KRW-MVL,BTC-MVL,KRW-STRAX,BTC-STRAX,KRW-AQT,BTC-AQT,KRW-GLM,BTC-GLM,KRW-SSX,BTC-SSX,KRW-META,BTC-META,KRW-FCT2,BTC-FCT2,KRW-CBK,BTC-CBK,KRW-SAND,BTC-SAND,KRW-HPO,BTC-HPO,KRW-DOGE,BTC-DOGE,KRW-STRIKE,BTC-STRIKE,KRW-PUNDIX,BTC-PUNDIX,KRW-FLOW,BTC-FLOW,KRW-AXS,BTC-AXS,KRW-STX,BTC-STX,KRW-SOL,BTC-SOL,KRW-MATIC,BTC-MATIC,KRW-AAVE,BTC-AAVE,KRW-1INCH,BTC-1INCH,KRW-ALGO,BTC-ALGO,KRW-NEAR,BTC-NEAR,KRW-AVAX,BTC-AVAX,KRW-T,BTC-T,KRW-CELO,BTC-CELO,KRW-GMT,BTC-GMT,KRW-APT,BTC-APT,KRW-MASK,BTC-MASK,KRW-ARB,BTC-ARB,KRW-EGLD,BTC-EGLD,KRW-SUI,BTC-SUI,KRW-GRT,BTC-GRT,KRW-BLUR,BTC-BLUR,KRW-IMX,BTC-IMX,KRW-SEI,BTC-SEI,KRW-MINA,BTC-MINA,KRW-CTC,BTC-CTC,KRW-ASTR,BTC-ASTR,KRW-ID,BTC-ID,KRW-PYTH,BTC-PYTH"
    response = requests.get(url)
    data = response.json()


    orderbook = {}

    # KRW-BTC
    orderbook[f"KRW_BTC_ASK"] = data[0]["orderbook_units"][0]["ask_price"]
    orderbook[f"KRW_BTC_BID"] = data[0]["orderbook_units"][0]["bid_price"]
    orderbook[f"KRW_BTC_BIDSIZE"] = data[0]["orderbook_units"][0]["bid_size"]
    orderbook[f"KRW_BTC_ASKSIZE"] = data[0]["orderbook_units"][0]["ask_size"]
    
    i = 1
    for crypto in cryptos:
        orderbook[f"KRW_{crypto}_ASK"] = data[i]["orderbook_units"][0]["ask_price"]
        orderbook[f"KRW_{crypto}_BID"] = data[i]["orderbook_units"][0]["bid_price"]
        orderbook[f"KRW_{crypto}_BIDSIZE"] = data[i]["orderbook_units"][0]["bid_size"]
        orderbook[f"KRW_{crypto}_ASKSIZE"] = data[i]["orderbook_units"][0]["ask_size"]

        i+=1
        orderbook[f"BTC_{crypto}_ASK"]  = data[i]["orderbook_units"][0]["ask_price"]
        orderbook[f"BTC_{crypto}_BID"]  = data[i]["orderbook_units"][0]["bid_price"]
        
        orderbook[f"BTC_{crypto}_ASKSIZE"]  = data[i]["orderbook_units"][0]["ask_size"]
        orderbook[f"BTC_{crypto}_BIDSIZE"]  = data[i]["orderbook_units"][0]["bid_size"]
        i+=1
    


    return orderbook

def print_oneway(code, orderbook, NEW_KRW_CODE, oneway_qty):
    print("one_way")
    print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")
    oneway_profit = round((NEW_KRW_CODE - orderbook[f"KRW_{code}_ASK"]) / orderbook[f"KRW_{code}_ASK"] * 100, 3)
    if oneway_profit > 0:
        print(f"{orderbook[f"KRW_{code}_ASK"]} ==> {NEW_KRW_CODE} (+{oneway_profit}%)")
    else:
        print(f"{orderbook[f"KRW_{code}_ASK"]} ==> {NEW_KRW_CODE} ({oneway_profit}%)")

    print(f"KRW_{code} qty : { orderbook[f"KRW_{code}_ASKSIZE"]} >= {oneway_qty[f"{code}_qty"]} ({orderbook[f"KRW_{code}_ASKSIZE"] >= oneway_qty[f"{code}_qty"]})")
    print(f"BTC_{code} qty : { orderbook[f"BTC_{code}_BIDSIZE"]} >= {oneway_qty[f"{code}_qty"]} ({orderbook[f"BTC_{code}_BIDSIZE"] >= oneway_qty[f"{code}_qty"]})")
    print(f"KRW_BTC qty : {orderbook["KRW_BTC_BIDSIZE"]} >= {oneway_qty["btc_qty"]} ({orderbook["KRW_BTC_BIDSIZE"] >= oneway_qty["btc_qty"]})")
    print(f"profit : {oneway_profit} > 0.35 ({oneway_profit > 0.35})\n")

    return oneway_profit

def print_otherway(code, orderbook, NEW_KRW_BTC, otherway_qty):
    print("\nother_way")
    print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
    otherway_profit = round((NEW_KRW_BTC - orderbook["KRW_BTC_ASK"]) / orderbook["KRW_BTC_ASK"] * 100, 3)
    if otherway_profit > 0:
        print(f"{orderbook["KRW_BTC_ASK"]} ==> {NEW_KRW_BTC} (+{otherway_profit}%)")
    else:
        print(f"{orderbook["KRW_BTC_ASK"]} ==> {NEW_KRW_BTC} ({otherway_profit}%)")

    print(f"KRW_BTC qty : {orderbook["KRW_BTC_ASKSIZE"]} >= {otherway_qty["btc_qty"]} ({orderbook["KRW_BTC_ASKSIZE"] >= otherway_qty["btc_qty"]})")
    print(f"BTC_{code} qty : {orderbook[f"BTC_{code}_ASKSIZE"]} > {otherway_qty[f"{code}_qty"]} ({orderbook[f"BTC_{code}_ASKSIZE"] > otherway_qty[f"{code}_qty"]})")
    print(f"KRW_{code} qty : {orderbook[f"KRW_{code}_BIDSIZE"]} > {otherway_qty[f"{code}_qty"]} ({orderbook[f"KRW_{code}_BIDSIZE"] > otherway_qty[f"{code}_qty"]})")
    print(f"profit : {otherway_profit} > 0.35 ({otherway_profit > 0.35})\n")

    return otherway_profit

def print_triangular_arbitrage(orderbook, available_qty, new_prices):
    expected_profits = {"oneway_profit" : {}, "otherway_profit" : {}}

    for crypto in cryptos:
        expected_profits["oneway_profit"][crypto] = print_oneway(crypto, orderbook, new_prices[f"NEW_KRW_{crypto}"], available_qty["oneway"])
        expected_profits["otherway_profit"][crypto] = print_otherway(crypto, orderbook, new_prices[f"NEW_KRW_BTC_{crypto}"], available_qty["otherway"])

    return expected_profits

def execute_triangular_arbitrage(krw, orderbook, available_qty, new_prices, expected_profits):
    # Checking Oneway 
    for crypto in cryptos:
        if (orderbook[f"KRW_{crypto}_BID"] < new_prices[f"NEW_KRW_{crypto}"]) and (orderbook[f"KRW_{crypto}_ASKSIZE"] >= available_qty["oneway"][f"{crypto}_qty"])  and (orderbook[f"BTC_{crypto}_BID"] * orderbook[f"BTC_{crypto}_BIDSIZE"] >= available_qty["oneway"]["btc_qty"]) and  (orderbook["KRW_BTC_BIDSIZE"] >= available_qty["oneway"]["btc_qty"]) and (expected_profits["oneway_profit"][crypto] > 0.35):
            one_way(crypto, krw, orderbook[f"KRW_{crypto}_ASK"], orderbook[f"BTC_{crypto}_BID"], orderbook["KRW_BTC_BID"], "limit")
            notify("oneway order executed")
            print(f"@ ONEWAY ORDER EXECUTED : {crypto}")
            return expected_profits["oneway_profit"]
    
        # Checking Otherway
        elif (orderbook["KRW_BTC_ASK"] < new_prices[f"NEW_KRW_BTC_{crypto}"]) and (orderbook[f"KRW_{crypto}_ASKSIZE"] >= available_qty["otherway"][f"{crypto}_qty"]) and (orderbook[f"BTC_{crypto}_ASKSIZE"] > available_qty["otherway"][f"{crypto}_qty"]) and (orderbook[f"KRW_{crypto}_BIDSIZE"] > available_qty["otherway"][f"{crypto}_qty"]) and (expected_profits["otherway_profit"][crypto] > 0.35):
            other_way(crypto, orderbook[f"KRW_{crypto}_BID"], orderbook[f"BTC_{crypto}_ASK"], orderbook["KRW_BTC_ASK"], "limit")
            notify("otherway order executed")
            print(f"@ OTHERWAY ORDER EXECUTED : {crypto}")
            return expected_profits["otherway_profit"]
        
    return 0


def get_available_qty(krw, orderbook):
    available_qty = {
        "oneway": {},
        "otherway": {}
    }

    for crypto in cryptos:
        available_qty["oneway"][f"{crypto}_qty"] = krw / orderbook[f"KRW_{crypto}_ASK"]
        available_qty["otherway"][f"{crypto}_qty"] = (krw / orderbook["KRW_BTC_ASK"]) / orderbook[f"BTC_{crypto}_ASK"]

    available_qty["oneway"]["btc_qty"] = available_qty["oneway"][f"{crypto}_qty"] * orderbook[f"BTC_{crypto}_BID"]
    available_qty["otherway"]["btc_qty"] = krw / orderbook["KRW_BTC_ASK"]

    return available_qty


def get_new_prices(orderbook):
    new_prices = {}
    
    for crypto in cryptos:
        new_prices[f"NEW_KRW_{crypto}"] = round(orderbook[f"BTC_{crypto}_BID"] * orderbook["KRW_BTC_BID"],2)
        new_prices[f"NEW_KRW_BTC_{crypto}"] = round(orderbook[f"KRW_{crypto}_BID"] / orderbook[f"BTC_{crypto}_ASK"],2)

    return new_prices


def balance_after_arbitrage(krw, profit):
    if profit != 0:
        krw = krw * (1 + profit / 100) * 0.9965
    return krw








