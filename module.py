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
  url = f"https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRW{code}"
  response = requests.get(url).json()
  currency = response[0]['basePrice']
  return currency



# Obtaining currency via Web Scraping
def get_currency_web_scraping(code):
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



# Live price data
def binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url)
        return float(response.json()["price"])
    except:
        raise SystemExit("Binance API banned in US IP")

def upbit_price(symbol):
    url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}"
    response = requests.get(url)
    data = response.json()[0]
    return float(data["trade_price"])

def bithumb_price(symbol):
    url = "https://api.bithumb.com/public/ticker/ALL_KRW"

    response = requests.get(url).text
    data = json.loads(response)

    return float(data['data'][symbol]['closing_price'])

def current_kimpga(symbol, currency):
    binance = binance_price(symbol) 
    upbit = upbit_price(symbol)  
    kimp = round(((upbit / (binance * currency)) - 1 ) * 100,2)
    print(f"KIMP: {kimp}\t Binance : {binance}\t UPBIT :{upbit}\n")
    return kimp, binance, upbit



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
    crypto_quantity = upbit.get_balance(symbol) - transaction_fee
    upbit_quantity = math.floor(crypto_quantity * 10000) / 10000
    print(f"\n{symbol} balance: {upbit_quantity:.4f} (Upbit)")
    return upbit_quantity


def BinanceUSDT():
    try:
        USDT = binance.fetch_balance()['free']['USDT']
        print(f"USDT balance : {USDT}")
        return USDT
    except:
        raise SystemExit("IP  not registered in binance")

def BinanceCRYPTO(symbol):
    crypto_quantity = binance.fetch_balance()['free'][symbol] 										 
    binance_quantity = '{:.6f}'.format(crypto_quantity)
    print(f"\n{symbol} balance : {binance_quantity} (Binance)")
    return float(binance_quantity)





# Withdraw/Deposit
def UpbitAddress(symbol):
    wallet = upbit.get_individual_deposit_address(symbol,symbol)
    address = wallet['deposit_address']
    tag = wallet['secondary_address']   
    return address,tag

def UpbitWithDraw(symbol,CRYPTO_AVAILABLE):
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
    address = binance.fetchDepositAddress(symbol)['address']
    tag = binance.fetchDepositAddress(symbol)['tag']
    return address,tag

def BinanceWithDraw(symbol,CRYPTO_AVAILABLE):
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




# Buy/Sell
def UpbitBUY(symbol,KRW_AVAILABLE):
    print(f"\nBuying {symbol} at UPBIT")
    upbit_buy = upbit.buy_market_order(f"KRW-{symbol}",KRW_AVAILABLE)
    print(upbit_buy) # 주문내역
    order_id = upbit_buy['uuid'] # 주문번호 저장
    order_state = upbit.get_individual_order(order_id)['state']
    
    # Wait until order is filled
    while order_state not in ['cancel', 'done']:
        print("Market Buy Order Taking place...")
        order_state = upbit.get_individual_order(order_id)['state']
    return order_id, order_state

def UpbitSELL(symbol,CRYPTO_AVAILABLE):
    print(f"Selling {symbol} at UPBIT")
    print(upbit.sell_market_order(f'KRW-{symbol}',CRYPTO_AVAILABLE))


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
        



# 역프매매
def Reverse(symbol,transaction_fee):
    print("---REVERSE----")

    # Check KRW balance 
    KRW = UpbitKRW()

    # Buy from UPBIT (Quantity : KRW)
    UpbitBUY(symbol,KRW)

    # Check crypto quantity
    UPBIT_CRYPTO = UpbitCRYPTO(symbol)

    # # Hedge 
    # KRW = 6016.419949
    # leverage,size = Hedge("upbit",symbol,KRW)
    
    # # UnHedge
    # UnHedge(symbol,leverage,size)
 
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
    








if __name__ == '__main__':
    start_time = time.time()

    print("--- %s seconds ---" % (time.time() - start_time))






###  SUB MODULES
def upbit_ticker_all():
    url = "https://api.upbit.com/v1/market/all"

    resp = requests.get(url)
    data = resp.json()

    krw_tickers = [coin['market'][4:] for coin in data if coin['market'].startswith("KRW")]

    return krw_tickers

# Risk Management
# - Hedge by adjusting short position size with leverage.
# - Adjust the minimum position size of crypto worth $5.021 with leverage.
# - Caution: High leverage when hedging may lead to potential blow-ups.
def Hedge(exchange,symbol,exchange_order):
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



###### CHECKING LIQUDITY ##########
def checkLiquidity(symbol, exchange="upbit"):    
    if exchange == "upbit":          
        url = f"https://api.upbit.com/v1/ticker?markets=KRW-{symbol}&markets=BTC-{symbol}&markets=KRW-BTC"
        response = requests.get(url)
        data = response.json()
          
        BTC = upbit_price("KRW-BTC")
        KRW_CODE = data[0]["acc_trade_price_24h"]
        BTC_CODE  = data[1]["acc_trade_price_24h"]*BTC
        KRW_BTC = data[2]["acc_trade_price_24h"]
        
        print(data[0]["market"], KRW_CODE)
        print(data[1]["market"], BTC_CODE)
        print(data[2]["market"], KRW_BTC)
        
        
        return  (KRW_CODE+BTC_CODE+KRW_BTC)/ 3



liquidity = {}

cryptos = upbit_ticker_all()

for crypto in cryptos:
	try:
		liquidity[crypto] = checkLiquidity("EOS")
	except:
		print(f"{crypto} : Unable to compute liquidity")
	print()


print("Unordered")
print(liquidity)

print("Ordered")
sorted_dict = dict(sorted(liquidity.items(), key=lambda item: item[1], reverse=True))

print(sorted_dict)

