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



# TransferArbitrage()

