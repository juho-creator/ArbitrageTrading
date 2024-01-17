from pprint import pprint
from module import * 
import time
import signal
import pyttsx3


engine = pyttsx3.init() # object creation

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female



# Auto Arbitrage Trading 
def TransferArbitrage():
    # Initializing parameters
    symbol = "EOS"
    reverse_percent = 2.8
    kimp_percent = 4

    # Get currency
    currency = get_currency_api("USD")


    exit_flag = False

    def signal_handler(signum, frame):
        nonlocal exit_flag
        exit_flag = True

    signal.signal(signal.SIGINT, signal_handler)


    while not exit_flag:
        
        start_time = time.time()

        kimp, binance, upbit = current_kimpga(symbol,currency)

        KRW = UpbitKRW()
        USDT = BinanceUSDT()

        Cash_at_upbit = KRW >= 6000
        Cash_at_binance = USDT >= 6
        
        if kimp <= reverse_percent and Cash_at_upbit: 
            Reverse(symbol,0)
            engine.say('reverse order filled')
            engine.runAndWait()
            
            

        elif kimp >= kimp_percent and Cash_at_binance:
            Kimp(symbol)
            engine.say('kimp order filled')
            engine.runAndWait()

        print("--- %s seconds ---" % (time.time() - start_time))


# Check Triangular Arbitrage for a crypto 
def checkTriangular(code="XRP"):
    print(f"\n{code}")
    a = upbit_price(f"KRW-{code}")
    b = upbit_price(f"BTC-{code}")
    c = upbit_price("KRW-BTC")

    print(f"KRW-{code} : " + str(a))
    print(f"BTC-{code} : " + str(b))
    print("KRW-BTC : " + str(c))

    d = round(b*c,2)

    if a<d:
        print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")
        profit = round((d-a)/a*100,2)
        print(f"{a} ==> {d} ({profit}%)")
        return True,profit
    else:
        print(f"BTC-{code} ==> KRW-BTC ==> KRW-{code}")
        profit = round((a-d)/d*100,2)
        print(f"{d} ==> {a} ({profit}%)")
        return False,profit


# Check Triangular Arbitrage for all crypto on upbit (10min)
def check_all_triangular():

    all = ['BTC', 'ETH', 'NEO', 'MTL', 'XRP', 'ETC', 'SNT', 'WAVES', 'XEM', 'QTUM', 'LSK', 'STEEM', 'XLM', 'ARDR', 'ARK', 'STORJ', 'GRS', 'ADA', 'SBD', 'POWR', 'BTG', 'ICX', 'EOS', 'TRX', 'SC', 'ONT', 'ZIL', 'POLYX', 'ZRX', 'LOOM', 'BCH', 'BAT', 'IOST', 'CVC', 'IQ', 'IOTA', 'HIFI', 'ONG', 'GAS', 'UPP', 'ELF', 'KNC', 'BSV', 'THETA', 
    'QKC', 'BTT', 'MOC', 'TFUEL', 'MANA', 'ANKR', 'AERGO', 'ATOM', 'TT', 'CRE', 'MBL', 'WAXP', 'HBAR', 'MED', 'MLK', 'STPT', 'ORBS', 'VET', 'CHZ', 'STMX', 'DKA', 'HIVE', 'KAVA', 'AHT', 'LINK', 'XTZ', 'BORA', 'JST', 'CRO', 'TON', 'SXP', 'HUNT', 'PLA', 'DOT', 'MVL', 'STRAX', 'AQT', 'GLM', 'SSX', 'META', 'FCT2', 'CBK', 'SAND', 'HPO', 'DOGE', 'STRK', 'PUNDIX', 'FLOW', 'AXS', 'STX', 'XEC', 'SOL', 'MATIC', 'AAVE', '1INCH', 'ALGO', 'NEAR', 'AVAX', 'T', 'CELO', 'GMT', 'APT', 'SHIB', 'MASK', 'ARB', 'EGLD', 'SUI', 'GRT', 'BLUR', 'IMX', 'SEI', 'MINA', 'CTC', 'ASTR']

    all_profits = {}

    for symbol in all: 
        try:
            direction,profit = checkTriangular(symbol)
            all_profits[symbol] = [direction,profit]
        except:
            print(f"{symbol} : No triangular arbitrage")

    sorted_dict = dict(sorted(all_profits.items(), key=lambda item: item[1][1], reverse=True))
    pprint(sorted_dict, sort_dicts=False)
    return sorted_dict


# Execute Triangular Arbitrage Trading
def TriangularArbitrage(symbol):
    one_way = checkTriangular(symbol)
    KRW = UpbitKRW()

    if one_way == True: 
        UBUY(f"KRW-{symbol}",KRW)

        crypto = UCRYPTO(symbol)
    
        USELL(f"BTC-{symbol}",crypto)

        BTC = UCRYPTO("BTC")
        USELL(f"KRW-BTC",BTC)

    elif one_way == False:
        UBUY(f"KRW-BTC",KRW)

        BTC = UCRYPTO("BTC")
        UBUY(f"BTC-{symbol}",BTC)

        crypto = UCRYPTO(symbol)
        USELL(f"KRW-{symbol}",crypto)




start_time = time.time()

arbitrage_opp = check_all_triangular()

test1 =  json.dumps(arbitrage_opp,indent=1)

f = open("arbitrage_opp.txt", "w")
f.write(str(test1))
f.close()

print("--- %s seconds ---" % (time.time() - start_time))



