import requests
from .upbit_user import *
from .upbit_module import *
import webbrowser




# Cryptos supporting triangular arbitrage
cryptos = [
    '1INCH', 'AAVE', 'ADA', 'AERGO', 'AHT', 'ALGO', 'ANKR', 'APT', 'AQT', 'ARB', 'ARDR', 'ARK', 'ASTR', 'ATOM', 'AVAX', 'AXS', 
    'BAT', 'BCH', 'BLUR', 'BORA', 'BSV', 'CBK', 'CELO', 'CHZ', 'CRO', 'CTC', 'CVC', 'DKA', 'DOGE', 'DOT', 'EGLD', 'ELF', 'EOS', 
    'ETC', 'ETH', 'FCT2', 'FLOW', 'GLM', 'GMT', 'GRS', 'GRT', 'HIFI', 'HIVE', 'HPO', 'HUNT', 'ID', 'IMX', 'IOST', 'IQ', 'JST', 
    'KAVA', 'LINK', 'LOOM', 'LSK', 'MANA', 'MASK', 'MATIC', 'MED', 'META', 'MINA', 'MLK', 'MOC', 'MTL', 'MVL', 'NEAR', 'ORBS', 
    'PDA', 'POLYX', 'POWR', 'PUNDIX', 'PYTH', 'QTUM', 'SAND', 'SBD', 'SC', 'SEI', 'SNT', 'SOL', 'STEEM', 'STMX', 'STORJ', 'STPT', 
    'STRAX', 'STRIKE', 'STX', 'SUI', 'SXP', 'T', 'TON', 'TRX', 'UPP', 'VET', 'WAVES', 'WAXP', 'XEM', 'XLM', 'XRP', 'XTZ', 'ZIL', 'ZRX'
]


# Directional orders
def oneway_market(symbol,KRW):
    # Market Orders
    crypto = upbit_buy(f"KRW-{symbol}", KRW)
    upbit_sell(f"BTC-{symbol}", crypto)
    BTC = crypto_balance("BTC")
    upbit_sell(f"KRW-BTC", BTC)

def oneway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, krw):
        volume = krw / KRW_CODE
        CODE_QTY = upbit_limit_buy(f"KRW-{symbol}", KRW_CODE, volume) 
        CODE_QTY = upbit_limit_sell(f"BTC-{symbol}", BTC_CODE, CODE_QTY*0.9997) 
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

def other_way(symbol,krw, KRW_CODE="", BTC_CODE="", KRW_BTC="",order_type="limit"):
    try:
        if order_type == "market":
            otherway_market(symbol,krw)
        elif order_type == "limit":
            otherway_limit(symbol, KRW_CODE, BTC_CODE, KRW_BTC, krw)
    except:
        pass



# 1. Get orderbook prices
def get_orderbook_prices():
    try:
        url = "https://api.upbit.com/v1/orderbook?markets=KRW-BTC,KRW-1INCH,BTC-1INCH,KRW-AAVE,BTC-AAVE,KRW-ADA,BTC-ADA,KRW-AERGO,BTC-AERGO,KRW-AHT,BTC-AHT,KRW-ALGO,BTC-ALGO,KRW-ANKR,BTC-ANKR,KRW-APT,BTC-APT,KRW-AQT,BTC-AQT,KRW-ARB,BTC-ARB,KRW-ARDR,BTC-ARDR,KRW-ARK,BTC-ARK,KRW-ASTR,BTC-ASTR,KRW-ATOM,BTC-ATOM,KRW-AVAX,BTC-AVAX,KRW-AXS,BTC-AXS,KRW-BAT,BTC-BAT,KRW-BCH,BTC-BCH,KRW-BLUR,BTC-BLUR,KRW-BORA,BTC-BORA,KRW-BSV,BTC-BSV,KRW-CBK,BTC-CBK,KRW-CELO,BTC-CELO,KRW-CHZ,BTC-CHZ,KRW-CRO,BTC-CRO,KRW-CTC,BTC-CTC,KRW-CVC,BTC-CVC,KRW-DKA,BTC-DKA,KRW-DOGE,BTC-DOGE,KRW-DOT,BTC-DOT,KRW-EGLD,BTC-EGLD,KRW-ELF,BTC-ELF,KRW-EOS,BTC-EOS,KRW-ETC,BTC-ETC,KRW-ETH,BTC-ETH,KRW-FCT2,BTC-FCT2,KRW-FLOW,BTC-FLOW,KRW-GLM,BTC-GLM,KRW-GMT,BTC-GMT,KRW-GRS,BTC-GRS,KRW-GRT,BTC-GRT,KRW-HIFI,BTC-HIFI,KRW-HIVE,BTC-HIVE,KRW-HPO,BTC-HPO,KRW-HUNT,BTC-HUNT,KRW-ID,BTC-ID,KRW-IMX,BTC-IMX,KRW-IOST,BTC-IOST,KRW-IQ,BTC-IQ,KRW-JST,BTC-JST,KRW-KAVA,BTC-KAVA,KRW-LINK,BTC-LINK,KRW-LOOM,BTC-LOOM,KRW-LSK,BTC-LSK,KRW-MANA,BTC-MANA,KRW-MASK,BTC-MASK,KRW-MATIC,BTC-MATIC,KRW-MED,BTC-MED,KRW-META,BTC-META,KRW-MINA,BTC-MINA,KRW-MLK,BTC-MLK,KRW-MOC,BTC-MOC,KRW-MTL,BTC-MTL,KRW-MVL,BTC-MVL,KRW-NEAR,BTC-NEAR,KRW-ORBS,BTC-ORBS,KRW-PDA,BTC-PDA,KRW-POLYX,BTC-POLYX,KRW-POWR,BTC-POWR,KRW-PUNDIX,BTC-PUNDIX,KRW-PYTH,BTC-PYTH,KRW-QTUM,BTC-QTUM,KRW-SAND,BTC-SAND,KRW-SBD,BTC-SBD,KRW-SC,BTC-SC,KRW-SEI,BTC-SEI,KRW-SNT,BTC-SNT,KRW-SOL,BTC-SOL,KRW-STEEM,BTC-STEEM,KRW-STMX,BTC-STMX,KRW-STORJ,BTC-STORJ,KRW-STPT,BTC-STPT,KRW-STRAX,BTC-STRAX,KRW-STRIKE,BTC-STRIKE,KRW-STX,BTC-STX,KRW-SUI,BTC-SUI,KRW-SXP,BTC-SXP,KRW-T,BTC-T,KRW-TON,BTC-TON,KRW-TRX,BTC-TRX,KRW-UPP,BTC-UPP,KRW-VET,BTC-VET,KRW-WAVES,BTC-WAVES,KRW-WAXP,BTC-WAXP,KRW-XEM,BTC-XEM,KRW-XLM,BTC-XLM,KRW-XRP,BTC-XRP,KRW-XTZ,BTC-XTZ,KRW-ZIL,BTC-ZIL,KRW-ZRX,BTC-ZRX"
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
    except Exception as e:
        print(e)



# 2. Compute available crypto quantity, new price, and expected profit
def get_available_qty(crypto, krw, orderbook):
    available_qty = {
        "oneway": {},
        "otherway": {}
    }

    available_qty["otherway"]["btc_qty"] = krw / orderbook["KRW_BTC_ASK"]

    available_qty["oneway"][f"{crypto}_qty"] = krw / orderbook[f"KRW_{crypto}_ASK"] 
    available_qty["oneway"]["btc_qty"] = available_qty["oneway"][f"{crypto}_qty"] * orderbook[f"BTC_{crypto}_BID"]
    available_qty["otherway"][f"{crypto}_qty"] = available_qty["otherway"]["btc_qty"] / orderbook[f"BTC_{crypto}_ASK"] #  crypto = btc * (crypto/btc) 

    return available_qty

def get_new_prices(crypto, orderbook):
    new_prices = {}

    new_prices[f"NEW_KRW_{crypto}"] = orderbook[f"BTC_{crypto}_BID"] * orderbook["KRW_BTC_BID"]
    new_prices[f"NEW_KRW_BTC_{crypto}"] = orderbook[f"KRW_{crypto}_BID"] / orderbook[f"BTC_{crypto}_ASK"]

    return new_prices

def get_expected_profit(crypto, orderbook, new_prices):
    expected_profits = {
        "oneway_profit": {},
        "otherway_profit": {}
    }
    
    expected_profits["oneway_profit"][crypto] = round((new_prices[f'NEW_KRW_{crypto}'] - orderbook[f"KRW_{crypto}_ASK"]) / orderbook[f"KRW_{crypto}_ASK"] * 100, 5)

    return expected_profits



# 3. Execute triangular arbitrage
def execute_triangular_arbitrage(crypto, krw, orderbook, available_qty, new_prices, expected_profits):
    # Checking Oneway 
    if (orderbook[f"KRW_{crypto}_ASK"] < new_prices[f"NEW_KRW_{crypto}"]) and (orderbook[f"KRW_{crypto}_ASKSIZE"] >= available_qty["oneway"][f"{crypto}_qty"])  and (orderbook[f"BTC_{crypto}_BIDSIZE"] >= available_qty["oneway"][f"{crypto}_qty"]) and  (orderbook["KRW_BTC_BIDSIZE"] >= available_qty["oneway"]["btc_qty"]) and (expected_profits["oneway_profit"][crypto] > 0.35):
        print(
            f"KRW_{crypto} price change : {orderbook[f'KRW_{crypto}_ASK']} < {new_prices[f'NEW_KRW_{crypto}']} ({orderbook[f'KRW_{crypto}_ASK'] < new_prices[f'NEW_KRW_{crypto}']})\n"
            f"KRW_{crypto} ask size : {orderbook[f'KRW_{crypto}_ASKSIZE']} >= {available_qty['oneway'][f'{crypto}_qty']} ({orderbook[f'KRW_{crypto}_ASKSIZE'] >= available_qty['oneway'][f'{crypto}_qty']})\n"
            f"BTC_{crypto} bid size : {orderbook[f'BTC_{crypto}_BIDSIZE']} >= {available_qty['oneway'][f'{crypto}_qty']} ({orderbook[f'BTC_{crypto}_BIDSIZE'] >= available_qty['oneway'][f'{crypto}_qty']})\n"
            f"KRW_BTC bid size : {orderbook['KRW_BTC_BIDSIZE']} >= {available_qty['oneway']['btc_qty']} ({orderbook['KRW_BTC_BIDSIZE'] >= available_qty['oneway']['btc_qty']})\n"
            f"Expected profit for {crypto} : {expected_profits['oneway_profit'][crypto]} > 0.35 ({expected_profits['oneway_profit'][crypto] > 0.35})"
        )
        url = f"https://api.upbit.com/v1/orderbook?markets=KRW-{crypto},BTC-{crypto},KRW-BTC"
        webbrowser.open(url)


        # one_way(crypto, krw, orderbook[f"KRW_{crypto}_ASK"], orderbook[f"BTC_{crypto}_BID"], orderbook["KRW_BTC_BID"], "limit")
        notify("oneway order executed")
        # print(f"@ ONEWAY ORDER EXECUTED : {crypto}")

    
        # # Checking Otherway
        # elif (orderbook["KRW_BTC_ASK"] < new_prices[f"NEW_KRW_BTC_{crypto}"]) and (orderbook[f"KRW_{crypto}_ASKSIZE"] >= available_qty["otherway"][f"{crypto}_qty"]) and (orderbook[f"BTC_{crypto}_ASKSIZE"] > available_qty["otherway"][f"{crypto}_qty"]) and (orderbook[f"KRW_{crypto}_BIDSIZE"] > available_qty["otherway"][f"{crypto}_qty"]) and (expected_profits["otherway_profit"][crypto] > 0.35):
        #     other_way(crypto, krw, orderbook[f"KRW_{crypto}_BID"], orderbook[f"BTC_{crypto}_ASK"], orderbook["KRW_BTC_ASK"], "limit")
        #     notify("otherway order executed")
        #     print(f"@ OTHERWAY ORDER EXECUTED : {crypto}")
        #     return expected_profits["otherway_profit"][crypto]
        


# Show computation status 
def print_oneway(crypto, orderbook, NEW_KRW_CODE, oneway_qty):
    print("one_way")
    print(f"KRW-{crypto} ==> BTC-{crypto} ==> KRW-BTC")
    oneway_profit = round((NEW_KRW_CODE - orderbook[f"KRW_{crypto}_ASK"]) / orderbook[f"KRW_{crypto}_ASK"] * 100, 3)
    # if oneway_profit > 0:
    #     print(f"{orderbook[f"KRW_{crypto}_ASK"]} ==> {NEW_KRW_CODE} (+{oneway_profit}%)")
    # else:
    #     print(f"{orderbook[f"KRW_{crypto}_ASK"]} ==> {NEW_KRW_CODE} ({oneway_profit}%)")

    # print(f"KRW_{crypto} qty : { orderbook[f"KRW_{crypto}_ASKSIZE"]} >= {oneway_qty[f"{crypto}_qty"]} ({orderbook[f"KRW_{crypto}_ASKSIZE"] >= oneway_qty[f"{crypto}_qty"]})")
    # print(f"BTC_{crypto} qty : { orderbook[f"BTC_{crypto}_BIDSIZE"]} >= {oneway_qty[f"{crypto}_qty"]} ({orderbook[f"BTC_{crypto}_BIDSIZE"] >= oneway_qty[f"{crypto}_qty"]})")
    # print(f"KRW_BTC qty : {orderbook["KRW_BTC_BIDSIZE"]} >= {oneway_qty["btc_qty"]} ({orderbook["KRW_BTC_BIDSIZE"] >= oneway_qty["btc_qty"]})")
    # print(f"profit : {oneway_profit} > 0.35 ({oneway_profit > 0.35})\n")

    return oneway_profit

def print_otherway(crypto, orderbook, NEW_KRW_BTC, otherway_qty):
    print("\nother_way")
    print(f"KRW-BTC ==> BTC-{crypto} ==> KRW-{crypto}")
    otherway_profit = round((NEW_KRW_BTC - orderbook["KRW_BTC_ASK"]) / orderbook["KRW_BTC_ASK"] * 100, 3)
    if otherway_profit > 0:
        print(f"{orderbook["KRW_BTC_ASK"]} ==> {NEW_KRW_BTC} (+{otherway_profit}%)")
    else:
        print(f"{orderbook["KRW_BTC_ASK"]} ==> {NEW_KRW_BTC} ({otherway_profit}%)")

    print(f"KRW_BTC qty : {orderbook["KRW_BTC_ASKSIZE"]} >= {otherway_qty["btc_qty"]} ({orderbook["KRW_BTC_ASKSIZE"] >= otherway_qty["btc_qty"]})")
    print(f"BTC_{crypto} qty : {orderbook[f"BTC_{crypto}_ASKSIZE"]} > {otherway_qty[f"{crypto}_qty"]} ({orderbook[f"BTC_{crypto}_ASKSIZE"] > otherway_qty[f"{crypto}_qty"]})")
    print(f"KRW_{crypto} qty : {orderbook[f"KRW_{crypto}_BIDSIZE"]} > {otherway_qty[f"{crypto}_qty"]} ({orderbook[f"KRW_{crypto}_BIDSIZE"] > otherway_qty[f"{crypto}_qty"]})")
    print(f"profit : {otherway_profit} > 0.35 ({otherway_profit > 0.35})\n")

    return otherway_profit



# Show balance after trading
def balance_after_arbitrage(krw, profit):
    if profit != 0:
        krw = krw * (1 + profit / 100) * 0.9965
    return krw
