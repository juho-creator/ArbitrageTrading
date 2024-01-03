from pprint import pprint
from module import * 
import time




# 역프매매
def Reverse(symbol,transaction_fee):
    # # Check KRW balance 
    # KRW = UpbitKRW()

    # # Buy from UPBIT (Quantity : KRW)
    # UpbitBUY(symbol,KRW)

    # # Check crypto quantity
    # UPBIT_CRYPTO = UpbitCRYPTO(symbol)

    # Hedge 
    KRW = 6016.419949
    leverage,size = Hedge("upbit",symbol,KRW)
    time.sleep(3)
    UnHedge(symbol,leverage,size)
    

    # # UnHedge
    # UnHedge(symbol,UPBIT_CRYPTO)
 
    # # Send to Binance (Quantity : XRP)
    # UpbitWithDraw(symbol,UPBIT_CRYPTO)
    
    # # Check crypto quantity (binance)
    # BINANCE_CRYPTO = BinanceCRYPTO(symbol)

    # # Sell at Binance (Quantity = XRP)
    # BinanceSEll(symbol,BINANCE_CRYPTO)
    




# 김프매매
def Kimp(symbol):
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
    


start_time = time.time()
Reverse("EOS",0)
print("--- %s seconds ---" % (time.time() - start_time))


