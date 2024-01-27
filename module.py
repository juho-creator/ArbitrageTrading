import requests
from bs4 import BeautifulSoup
import time
from pprint import pprint
import json
import ccxt
import pyupbit
import math
from config import *
import pandas as pd 
from decimal import Decimal


UPBIT_TICKERS = ['BTC', 'ETH', 'NEO', 'MTL', 'XRP', 'ETC', 'SNT', 'WAVES', 'XEM', 'QTUM', 'LSK', 'STEEM', 'XLM', 'ARDR', 'ARK', 'STORJ', 'GRS', 'ADA', 'SBD', 'POWR', 'BTG', 'ICX', 'EOS', 'TRX', 'SC', 'ONT', 'ZIL', 'POLYX', 'ZRX', 'LOOM', 'BCH', 'BAT', 'IOST', 'CVC', 'IQ', 'IOTA', 'HIFI', 'ONG', 'GAS', 'UPP', 'ELF', 'KNC', 'BSV', 'THETA', 
'QKC', 'BTT', 'MOC', 'TFUEL', 'MANA', 'ANKR', 'AERGO', 'ATOM', 'TT', 'CRE', 'MBL', 'WAXP', 'HBAR', 'MED', 'MLK', 'STPT', 'ORBS', 'VET', 'CHZ', 'STMX', 'DKA', 'HIVE', 'KAVA', 'AHT', 'LINK', 'XTZ', 'BORA', 'JST', 'CRO', 'TON', 'SXP', 'HUNT', 'PLA', 'DOT', 'MVL', 'STRAX', 'AQT', 'GLM', 'SSX', 'META', 'FCT2', 'CBK', 'SAND', 'HPO', 'DOGE', 'STRK', 'PUNDIX', 'FLOW', 'AXS', 'STX', 'XEC', 'SOL', 'MATIC', 'AAVE', '1INCH', 'ALGO', 'NEAR', 'AVAX', 'T', 'CELO', 'GMT', 'APT', 'SHIB', 'MASK', 'ARB', 'EGLD', 'SUI', 'GRT', 'BLUR', 'IMX', 'SEI', 'MINA', 'CTC', 'ASTR']



#  API SETUP (remove  any duplicate parameters)
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)
api_params = {
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True, # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'adjustForTimeDifference': True,
    },
}

binance = ccxt.binance({**api_params, 'options': {'defaultType': 'spot','adjustForTimeDifference': True}})
binance_futures = ccxt.binance({**api_params, 'options': {'defaultType': 'future','adjustForTimeDifference': True }})

# TESTNET API setup
binance_futures_test = ccxt.binance({
    'apiKey': TEST_KEY,
    'secret': TEST_SECRET,
    'enableRateLimit': True,  # https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'defaultType': 'future',
        'adjustForTimeDifference': True,
    },
})
binance_futures_test.set_sandbox_mode(True)  # comment if you're not using the testnet



# Obtaining currency via API
def get_currency_api(code):
    try:
        url = f"https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRW{code}"
        response = requests.get(url).json()
        currency = response[0]['basePrice']
        return currency
    except:
        print("Unable to retrieve currency")
    



# Obtaining currency via Web Scraping
def get_currency_web_scraping(code):
    try:
        url = f'https://m.stock.naver.com/marketindex/exchange/FX_{code}KRW'
        headers = {'Accept-Language': 'ko-KR', 'User-Agent': 'Mozilla/5.0'}

        # HTTP request & response from Naver
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parsing HTML response data with lxml for better performance
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract exchange rate using a more specific selector
            exchange_rate_tag = soup.select_one('strong.DetailInfo_price__I_VJn')

            # Check if the tag is found
            if exchange_rate_tag:
                # Extract text from the tag and clean it up
                exchange_rate = exchange_rate_tag.get_text(strip=True).replace("KRW", "").replace(",", "")

                # Convert the cleaned-up string to a float
                exchange_rate = float(exchange_rate)
                # print(f"{currency_code}KRW = {exchange_rate}")
                return exchange_rate
    except:
        print("Unable to retrieve currency")



# Live price data
def binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url)
        return float(response.json()["price"])
    except Exception as e:
        print(e)
        raise SystemExit("Binance API banned in US IP")
    

def upbit_price(symbol):
    try:
        url = f"https://api.upbit.com/v1/ticker?markets={symbol}"
        response = requests.get(url)
        data = response.json()[0]
        return float(data["trade_price"])
    except:
        print(f"Unable to get {symbol} price")

def bithumb_price(symbol):
    try:
        url = f"https://api.bithumb.com/public/ticker/{symbol}"

        response = requests.get(url).text
        data = json.loads(response)
        return float(data['data']['prev_closing_price'])
    except:
        print(f"Unable to get {symbol} price")

													   


# Kimp computation
def current_kimpga(symbol, currency):
    try:
        binance = binance_price(symbol) 
        upbit = upbit_price(f"KRW-{symbol}")  
        
        foreign_exchange = binance * currency
        
        if upbit > foreign_exchange:
            kimp = round(((upbit / foreign_exchange) - 1) * 100,2)
            print(f"KIMP: {kimp}\t Binance : {binance}\t UPBIT :{upbit}\n")
            return kimp, binance, upbit
        
        elif foreign_exchange > upbit:
            kimp = round(((foreign_exchange / upbit) - 1) * 100,2)
            print(f"KIMP: {kimp}\t Binance : {binance}\t UPBIT :{upbit}\n")
            return kimp, binance, upbit

        
    except:
        print(f"Unable to compute Kimp")

def get_all_kimp():
    df = pd.DataFrame()

    currency = get_currency_api("USD")

    for crypto in UPBIT_TICKERS:
        try:
            print(f"\n{crypto}")
            kimp, binance,upbit = current_kimpga(crypto,currency)
            data = {'symbol': crypto, 'KIMP': kimp, 'Binance': binance, 'UPBIT': upbit}
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        except:
            print(f"{crypto} doesn't exist on binance")
    df.to_csv('output.csv', index=False)


# Triangualr Arbitrage
# def upbitTriangular(code):
#     url = f"https://api.upbit.com/v1/orderbook?markets=KRW-{code}&markets=BTC-{code}&markets=KRW-BTC"
#     response = requests.get(url)
#     data = response.json()
        
#     KRW_CODE = data[0]["trade_price"]
#     BTC_CODE  = data[1]["trade_price"]
#     KRW_BTC = data[2]["trade_price"]
    
#     print(data[0]["market"], KRW_CODE)
#     print(data[1]["market"], BTC_CODE)
#     print(data[2]["market"], KRW_BTC)

#     KRW_NEW_CODE = round(BTC_CODE*KRW_BTC,2)

#     if KRW_CODE < KRW_NEW_CODE:
#         print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")
#         profit = round((KRW_NEW_CODE-KRW_CODE)/KRW_CODE*100,2)
#         print(f"{KRW_CODE} ==> {KRW_NEW_CODE} ({profit}%)")
#         return True,profit,KRW_CODE,BTC_CODE,KRW_BTC
#     else:
#         print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
#         profit = round((KRW_CODE-KRW_NEW_CODE)/KRW_NEW_CODE*100,2)
#         print(f"{KRW_NEW_CODE} ==> {KRW_CODE} ({profit}%)")
#         return False,profit,KRW_CODE,BTC_CODE,KRW_BTC
import pyttsx3
engine = pyttsx3.init() # object creation

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female



def upbitTriangular(code):
    url = f"https://api.upbit.com/v1/orderbook?markets=KRW-{code}&markets=BTC-{code}&markets=KRW-BTC"
    response = requests.get(url)
    data = response.json()
        
    KRW_CODE_ask = data[0]["orderbook_units"][0]["ask_price"]
    KRW_CODE_bid = data[0]["orderbook_units"][0]["bid_price"]

    BTC_CODE_ask  = data[1]["orderbook_units"][0]["ask_price"]
    BTC_CODE_bid  = data[1]["orderbook_units"][0]["bid_price"]

    KRW_BTC_ask = data[2]["orderbook_units"][0]["ask_price"]
    KRW_BTC_bid = data[2]["orderbook_units"][0]["bid_price"]
    
    # print(data[0]["market"], KRW_CODE_bid,KRW_CODE_ask)
    # print(data[1]["market"], BTC_CODE_bid,BTC_CODE_ask)
    # print(data[2]["market"], KRW_BTC_bid, KRW_BTC_ask)

    if (KRW_CODE_ask < (BTC_CODE_bid * KRW_BTC_bid)):
        print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")        
        higher_price = BTC_CODE_bid * KRW_BTC_bid
        print(f"{KRW_CODE_ask} ==> {BTC_CODE_bid} * {KRW_BTC_bid} = {higher_price} ({(higher_price-KRW_CODE_ask)/KRW_CODE_ask*100}%)")
        engine.say(f'{code} one way executed')
        OneWay(code,KRW_CODE_ask,BTC_CODE_bid,KRW_BTC_bid)



    elif (KRW_BTC_ask < (BTC_CODE_ask * KRW_CODE_bid)):
        print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
        higher_price = BTC_CODE_ask * KRW_CODE_bid
        print(f"{KRW_BTC_ask} ==> {BTC_CODE_ask} * {KRW_CODE_bid} = {higher_price} ({(higher_price-KRW_BTC_ask)/KRW_BTC_ask*100}%)")
        engine.say(f'{code} other way executed')
        OtherWay(code,KRW_BTC_ask,BTC_CODE_ask,KRW_CODE_bid)




def binanceTriangular(code):
    USDT_CODE = binance_price(f"{code}USDT")
    BTC_CODE = binance_price(f"{code}BTC")
    USDT_BTC = binance_price("BTCKRW")

    print(f"KRW-{code} : " + str(USDT_CODE))
    print(f"BTC-{code} : " + str(BTC_CODE))
    print("KRW-BTC : " + str(USDT_BTC))

    KRW_NEW_CODE = round(BTC_CODE*USDT_BTC,2)

    if USDT_CODE < KRW_NEW_CODE:
        print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")
        profit = round((KRW_NEW_CODE-USDT_CODE)/USDT_CODE*100,2)
        print(f"{USDT_CODE} ==> {KRW_NEW_CODE} ({profit}%)")
        return True,profit,USDT_CODE,BTC_CODE,USDT_BTC
    else:
        print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
        profit = round((USDT_CODE-KRW_NEW_CODE)/KRW_NEW_CODE*100,2)
        print(f"{KRW_NEW_CODE} ==> {USDT_CODE} ({profit}%)")
        return False,profit,USDT_CODE,BTC_CODE,USDT_BTC

def checkTriangular(code="XRP",exchange="upbit"):
    print(f"\n{code}")
    if exchange == "upbit":
        one_way,profit,KRW_CODE,BTC_CODE,KRW_BTC = upbitTriangular(code)
        return one_way,profit,KRW_CODE,BTC_CODE,KRW_BTC

    elif exchange == "binance":
        one_way,profit,USDT_CODE,BTC_CODE,USDT_BTC = binanceTriangular(code)
        return one_way,profit,USDT_CODE,BTC_CODE,USDT_BTC

def check_all_triangular():
    all_profits = {}

    for symbol in UPBIT_TICKERS: 
        try:
            direction,profit = checkTriangular(symbol)
            all_profits[symbol] = [direction,profit]
        except:
            print(f"{symbol} : No triangular arbitrage")

    sorted_dict = dict(sorted(all_profits.items(), key=lambda item: item[1][1], reverse=True))
    pprint(sorted_dict, sort_dicts=False)
    return sorted_dict

def record_all_triangular():
    arbitrage_opp = check_all_triangular()

    test1 =  json.dumps(arbitrage_opp,indent=1)

    f = open("arbitrage_opp.txt", "w")
    f.write(str(test1))
    f.close()

    



def OneWay(symbol,KRW_CODE,BTC_CODE,KRW_BTC):
    KRW = UpbitKRW()

    volume = KRW / KRW_CODE
    Upbit_LIMIT_BUY(f"KRW-{symbol}",KRW_CODE,volume)
    # UpbitBUY(f"KRW-{symbol}",KRW)

    crypto = UCRYPTO(symbol)
    Upbit_LIMIT_SELL(f"BTC-{symbol}",BTC_CODE,crypto)
    # UpbitSELL(f"BTC-{symbol}",crypto)

    BTC = UCRYPTO("BTC")
    Upbit_LIMIT_SELL(f"KRW-BTC",KRW_BTC,BTC)
    # UpbitSELL(f"KRW-BTC",BTC)

def OtherWay(symbol,KRW_CODE,BTC_CODE,KRW_BTC):
    KRW = UpbitKRW()

    volume = KRW / KRW_CODE
    Upbit_LIMIT_BUY(f"KRW-BTC",KRW_BTC,volume)
    # UpbitBUY(f"KRW-BTC",KRW)

    BTC = UCRYPTO("BTC")*0.9975
    Upbit_LIMIT_BUY(f"BTC-{symbol}",BTC_CODE,BTC)
    # UpbitBUY(f"BTC-{symbol}",BTC)

    crypto = UCRYPTO(symbol)
    Upbit_LIMIT_SELL(f"KRW-{symbol}",KRW_CODE,crypto)
    # UpbitSELL(f"KRW-{symbol}",crypto)



# Check Balance
def UpbitKRW():
    KRW = upbit.get_balance("KRW") 
    print(f"KRW balance : {KRW}")
    try:
        KRW_AVAILABLE = '{:.6f}'.format(KRW * 0.995)
        print(f"Available KRW balance : {KRW_AVAILABLE}\n")
    except TypeError:
        raise SystemExit("IP not registered in UPBIT")

    return float(KRW_AVAILABLE)

def UpbitCRYPTO(symbol, transaction_fee=0):
    try:
        crypto_quantity = upbit.get_balance(symbol) - transaction_fee
        upbit_quantity = math.floor(crypto_quantity * 10000) / 10000
        print(f"\n{symbol} balance: {upbit_quantity:.4f} (Upbit)")
        return upbit_quantity
    except:
        print(f"Unable to retrieve {symbol} balance (Upbit)")

def UCRYPTO(symbol, transaction_fee=0):
    try:
        crypto_quantity = upbit.get_balance(symbol) - transaction_fee
  
        print(f"\n{symbol} balance: {crypto_quantity:.8f} (Upbit)")
        return crypto_quantity
    except:
        print(f"Unable to retrieve {symbol} balance (Upbit)")



def BinanceUSDT():
    try:
        USDT = binance.fetch_balance()['free']['USDT']
        print(f"USDT balance : {USDT}")
        return USDT
    except Exception as e:
        print(e)
        raise SystemExit("IP  not registered in binance")

def BinanceCRYPTO(symbol):
    try:
        crypto_quantity = binance.fetch_balance()['free'][symbol] 										 
        binance_quantity = '{:.6f}'.format(crypto_quantity)
        print(f"\n{symbol} balance : {binance_quantity} (Binance)")
        return float(binance_quantity)
    except:
        print(f"Unable to retrieve {symbol} balance (Binance)")




# Withdraw/Deposit
def UpbitAddress(symbol):
    try:
        wallet = upbit.get_individual_deposit_address(symbol,symbol)
        address = wallet['deposit_address']
        tag = wallet['secondary_address']   
        return address,tag
    except:
        print(f"{symbol} wallet not found")

def UpbitWithDraw(symbol,CRYPTO_AVAILABLE):
    try:
        print(f"\nWithdrawing {symbol} (UPBIT -> Binance)")
        address,tag = BinanceAddress(symbol)
        upbit_send = upbit.withdraw_coin(symbol,symbol,CRYPTO_AVAILABLE,address,tag)
        pprint(upbit_send)
        transaction_id = upbit_send['uuid']

        transaction_state = upbit.get_individual_withdraw_order(transaction_id,symbol)['state']
        while(transaction_state!='DONE'):
            print(f"Transfering {symbol}.... (UPBIT --> Binance)")
            try: 
                transaction_state = upbit.get_individual_withdraw_order(transaction_id,symbol)['state']
            except Exception as e:
                print(e)
        print("Successfully sent to Binance")

        return transaction_id,transaction_state
    except:
        print(f"Unable to withdraw {symbol} from Upbit")

def UpbitRECEIVED(txid,symbol,quantity):
    deposit_state = 'None'

    while (deposit_state != 'ACCEPTED'):
        try:
            deposit_state = upbit.get_individual_deposit_order(txid,symbol)['state']
            pprint(deposit_state)
            print("Confirming at UPBIT...")
        except:
            print("Waiting at UPBIT...")
    print("Received at UPBIT!")
    UPBIT_CRYPTO = UpbitCRYPTO(symbol)
    while(UPBIT_CRYPTO < quantity):
        print('Waiting for UPBIT balance to be updated')
        UPBIT_CRYPTO = UpbitCRYPTO(symbol)
    
    return UPBIT_CRYPTO


def BinanceAddress(symbol):
    try:
        address = binance.fetchDepositAddress(symbol)['address']
        tag = binance.fetchDepositAddress(symbol)['tag']
        return address,tag
    except:
        print(f"{symbol} wallet not found")

def BinanceWithDraw(symbol,CRYPTO_AVAILABLE):
    try:
        address, tag = UpbitAddress(symbol)

        withdrawal = binance.withdraw(
            symbol, CRYPTO_AVAILABLE, address,tag, {f'chain': {symbol}})
        print(f"\nWithdrawing {symbol} (Binance -> UPBIT)")
        print(withdrawal)

        TXID = None
        while(TXID == None):
            print(f"Transfering {symbol} (Binance -> UPBIT)")
            withdraw = binance.fetchWithdrawals(symbol,limit=1)
            pprint(withdraw)
            TXID = withdraw[0]['txid']
            quantity = withdraw[0]['amount']
        print("Successfully sent to UPBIT")
        return TXID,quantity
    except:
        print(f"Unable to withdraw {symbol} from Binance")




# MARKET Buy/Sell
def UpbitBUY(symbol,volume):
    try:
        print(f"\nBuying {symbol} at UPBIT")
        upbit_buy = upbit.buy_market_order(f"{symbol}",volume)
        print(upbit_buy) # 주문내역
        order_id = upbit_buy['uuid'] # 주문번호 저장
															   
	
								
												
												 
        order_state = upbit.get_individual_order(order_id)['state']
        
        # Wait until order is filled
        while order_state not in ['cancel', 'done']:
            print("Market Buy Order Taking place...")
            order_state = upbit.get_individual_order(order_id)['state']
        return order_id, order_state
    except Exception as e:
        print(f"Unable to buy {symbol} (Upbit)")
        print(e)

def UpbitSELL(symbol,CRYPTO_AVAILABLE):
    try:
        print(f"Selling {symbol} at UPBIT")
        upbit_sell = upbit.sell_market_order(f'{symbol}',CRYPTO_AVAILABLE)
        print(upbit_sell)
        order_id = upbit_sell['uuid'] # 주문번호 저장
        order_state = upbit.get_individual_order(order_id)['state']
        print(order_state)

        # Wait until order is filled
        while order_state not in ['cancel','done']:
            order_state = upbit.get_individual_order(order_id)['state']
            print(upbit_sell)
        return order_id, order_state
        
    except Exception as e:
        print(f"Unable to sell {symbol} (Upbit)")
        print(e)

def BinanceBUY(symbol,USDT):
    print(f"\nBuying {symbol} at Binance")
    try:
        buy_binance = binance.create_market_buy_order(f"{symbol}USDT", USDT)

        order_id = buy_binance['info']['orderId']
        order_status = binance.fetchOrder(order_id, symbol+"USDT")['status']
        while(order_status != 'closed'):
            print(f"Buying {symbol} from Binance...")
            order_status = binance.fetchOrder(order_id,symbol+"USDT")['status']
        print(f"Bought {symbol} from Binance")
    except:
        print("ORDER FAILED : Total order value should be more than 5 USDT")

def BinanceSEll(symbol,CRYPTO_AVAILABLE):
    print(f"Selling {symbol} at Binance")
    try:
        print(binance.create_market_sell_order(f"{symbol}USDT", CRYPTO_AVAILABLE))
    except:
        print("ORDER FAILED : Total order value should be more than 5 USDT")
        

# LIMIT Buy/Sell
def Upbit_LIMIT_BUY(symbol,price,volume):
    try:
        print(f"\nBuying {symbol} at UPBIT")
        upbit_buy = upbit.buy_limit_order(f"{symbol}",price,volume)
        print(upbit_buy) # 주문내역
        order_id = upbit_buy['uuid'] # 주문번호 저장
        order_state = upbit.get_individual_order(order_id)['state']
        
        # Wait until order is filled
        while order_state not in ['cancel', 'done']:
            print("Limit Buy Order Taking place...")
            order_state = upbit.get_individual_order(order_id)['state']
        return order_id, order_state
    except Exception as e:
        print(f"Unable to buy {symbol} (Upbit)")
        print(e)

def Upbit_LIMIT_SELL(symbol,price,volume):
    try:
        print(f"Selling {symbol} at UPBIT")
        upbit_sell = upbit.sell_limit_order(f'{symbol}',price,volume)
        print(upbit_sell)
        order_id = upbit_sell['uuid'] # 주문번호 저장
        order_state = upbit.get_individual_order(order_id)['state']

        # Wait until order is filled
        while order_state not in ['cancel','done']:
            print("Limit Sell Order Taking place...")
            order_state = upbit.get_individual_order(order_id)['state']
            print(order_state)
        return order_id, order_state
        
    except Exception as e:
        print(f"Unable to sell {symbol} (Upbit)")
        print(e)




# 역프매매
def Reverse(symbol,transaction_fee):
    print("---REVERSE----")

    # Check KRW balance 
    KRW = UpbitKRW()

    # Buy from UPBIT (Quantity : KRW)
    UpbitBUY(symbol,KRW)

    # Check crypto quantity
    UPBIT_CRYPTO = UpbitCRYPTO(symbol)

			  
					   
											   
	
			   
								   
 
    # Send to Binance (Quantity : XRP)
    UpbitWithDraw(symbol,UPBIT_CRYPTO)
    
    # Check crypto quantity (binance)
    BINANCE_CRYPTO = BinanceCRYPTO(symbol)

    # Sell at Binance (Quantity = XRP)
    BinanceSEll(symbol,BINANCE_CRYPTO)
    
# 김프매매
def Kimp(symbol):
    print("---KIMP---")

    # Check USDT balance
    USDT = BinanceUSDT()

    # Buy at Binance (Quantity : USDT)
    BinanceBUY(symbol,USDT)

    # Check crypto quantity
    BINANCE_CRYPTO = BinanceCRYPTO(symbol)
																											 																
    # Send to UPBIT (Quantity : XRP)
    TXID, quantity = BinanceWithDraw(symbol,BINANCE_CRYPTO)

    # Check if received from UPBIT
    UPBIT_CRYPTO = UpbitRECEIVED(TXID,symbol,quantity)

    # Sell from UPBIT (Quantity : XRP)
    UpbitSELL(symbol,UPBIT_CRYPTO)
    

def TriangularArbitrage(symbol):
    upbit_price(symbol)






###  SUB MODULES
def upbit_ticker_all():
    url = "https://api.upbit.com/v1/market/all"

    resp = requests.get(url)
    data = resp.json()

    krw_tickers = [coin['market'][4:] for coin in data if coin['market'].startswith("KRW")]

    return krw_tickers




def upbit_global_ticker_all(country):
    if country == "SG":
        url = "https://sg-api.upbit.com/v1/market/all"

    elif country == "ID": 
        url = "https://id-api.upbit.com/v1/market/all"
    elif country == "TH": 
        url = "https://th-api.upbit.com/v1/market/all"

    resp = requests.get(url)
    data = resp.json()# UPBIT Singapore
    return data

																						   

					  

 
# Risk Management
# - Hedge by adjusting short position size with leverage.
# - Adjust the minimum position size of crypto worth $5.021 with leverage.
# - Caution: High leverage when hedging may lead to potential blow-ups.
def Hedge(exchange,symbol,exchange_order):
    # # Hedge 
    # KRW = 6016.419949
    # leverage,size = Hedge("upbit",symbol,KRW)


    #  Set initial cash for calculation
    MIN_ORDER = 6
    if exchange == "upbit":  # KRW -> USD
        exchange_order = exchange_order / get_currency_api("USD")      
          
    # Calculate Leverage 
    LEVERAGE = round(exchange_order/MIN_ORDER)
    if LEVERAGE == 0: # x0 -> x1
        LEVERAGE = 1

    # Calculate minimum position size 
    MIN_SIZE = MIN_ORDER / binance_futures_test.fetch_ticker(f"{symbol}/USDT")['last']

    # Hedge
    try :
        binance_futures_test.set_leverage(LEVERAGE,f"{symbol}/USDT")
        pprint(binance_futures_test.create_market_sell_order(f"{symbol}/USDT",MIN_SIZE))
        print("Hedged!")
        print(f"Leverage : {LEVERAGE}, size : {MIN_SIZE}")
    except Exception as e:
        print(e)    

    return LEVERAGE,MIN_SIZE



def UnHedge(symbol,leverage,size):
    # # UnHedge
    # UnHedge(symbol,leverage,size)

    try: 
        pprint(binance_futures_test.create_market_buy_order(f"{symbol}/USDT",size))
        print("Unhedged!")
        print(f"Leverage : {leverage}, size : {size}")
    except Exception as e:
        print(e)
        



# Backtest Modules
def binance_test(symbol,period):
    bnc_ohlcv = binance.fetch_ohlcv(f"{symbol}/USDT",period)
    df = pd.DataFrame(bnc_ohlcv,columns=['datetime','open', 'high', 'low','close','volume'])
    df.set_index('datetime', inplace=True)
    return df

def current_kimpga_test(exchange_buy,exchange_sell, symbol, currency):
    if exchange_buy == exchange_sell:
        print("Cannot compute kimp for identical exchanges")
        return
    
    # Exchange Buy
    if exchange_buy == "binance":
        buy_price = binance_price(symbol,currency)
    elif exchange_buy == "upbit":
        buy_price = upbit_price(symbol)
    elif exchange_buy == "bithumb":
        buy_price = bithumb(symbol)

    # Exchange Sell
    if exchange_sell == "binance":
        sell_price = binance_price(symbol,currency)
    elif exchange_sell == "upbit":
        sell_price = upbit_price(symbol)
    elif exchange_sell == "bithumb":
        sell_price = bithumb(symbol)
    
    # Calculate Kimp
    if sell_price is not None and buy_price is not None:
        print(f"{symbol} price on {exchange_buy}: ₩ {buy_price}")
        print(f"{symbol} price on {exchange_sell}: ₩ {sell_price}")

        kimp = round(((sell_price / buy_price) - 1) * 100,2)
        print(f"Kimp {symbol}: {kimp} %")

        if kimp > 0:
            return kimp, buy_price, sell_price  # 김프
        else:
            return kimp, buy_price, sell_price  # 역프
   




def upbit_global_price(symbol,country):
    try:
        if country == "SG":
            url = f"https://sg-api.upbit.com/v1/ticker?markets=SGD-{symbol}" # UPBIT Singapore
        elif country == "TH":
            url = f"https://th-api.upbit.com/v1/ticker?markets=THB-{symbol}" # UPBIT Thailand
        elif country == "ID":
            url = f"https://id-api.upbit.com/v1/ticker?markets=IDR-{symbol}" # UPBIT Indonesia

        response = requests.get(url)
        data = response.json()[0]
        return float(data["trade_price"])
    except:
        print(f"Unable to get {symbol} price from {country}")



    

# OKX
# Bybit
# Binance
# BitMEX
# Bitget
# Crypto.com
# HTX





def exchange_price_diff(code="BTC"):
        prices_dict = {
            "KR": upbit_price("KRW-{code}"),
            "SG": upbit_global_price(code, "SG") * get_currency_api("SGD"),
            "TH": upbit_global_price(code, "TH") * get_currency_api("THB"),
            "ID": upbit_global_price(code, "ID") * get_currency_api("IDR") / 100
        }

        prices_sorted_dict = dict(sorted(prices_dict.items(), key=lambda item: item[1], reverse=True))

        pprint(prices_sorted_dict)

        for currency1, price1 in prices_sorted_dict.items():
            for currency2, price2 in prices_sorted_dict.items():
                if currency1 != currency2:
                    percentage_diff = ((price1 - price2) / price2) * 100
                    print(f"{currency2} -> {currency1}: {percentage_diff:.2f}%")




# Check Liquidity

def checkLiquidity(symbol, exchange="upbit"):    
    if exchange == "upbit":          
        url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}&markets=BTC-{symbol}&markets=KRW-BTC"
        data = requests.get(url).json()
							  
          
        BTC = data[2]["trade_price"]
        KRW_BTC = data[2]["acc_trade_price_24h"]
        KRW_CODE = data[0]["acc_trade_price_24h"]
        BTC_CODE  = data[1]["acc_trade_price_24h"]*BTC
												
        
        print(data[0]["market"], KRW_CODE)
        print(data[1]["market"], BTC_CODE)
        print(data[2]["market"], KRW_BTC)
        
        
        return  (KRW_CODE+BTC_CODE+KRW_BTC)/ 3


def checkAllLiquidity():
    liquidity = {}

    cryptos = upbit_ticker_all()

    for crypto in cryptos:
        try:
            liquidity[crypto] = checkLiquidity(crypto)
        except:
            print(f"{crypto} : Unable to compute liquidity")
        print()

    sorted_dict = dict(sorted(liquidity.items(), key=lambda item: item[1], reverse=True))
    pprint(sorted_dict,sort_dicts=False)
										   
					

if __name__ == '__main__':
    start_time = time.time()
    symbol = "EOS"
    url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}&markets=BTC-{symbol}&markets=KRW-BTC"
    data = requests.get(url).json()
          
    BTC = data[2]["trade_price"]
    print("--- %s seconds ---" % (time.time() - start_time))
