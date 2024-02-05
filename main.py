from arbitrage_trading import *
import time





start_time = time.time()

while(1):
    cryptos = available_cryptos
    for crypto in cryptos:
        print(f"\n\n{crypto}")
        upbit_triangular(crypto)




print("--- %s seconds ---" % (time.time() - start_time))

