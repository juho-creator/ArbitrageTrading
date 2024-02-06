from arbitrage_trading import *
import time
import pyttsx3



def upbit_triangular_roundtrip(krw):
    start_time = time.time()
    # notify(f"Starting arbitrage detection {i+1}")
    print(f"Starting arbitrage detection {i+1}")
    cryptos = available_cryptos
    for crypto in cryptos:
        print(f"\n\n{crypto}")
        krw = upbit_triangular(crypto, krw)
    # notify("Arbitrage detection completed")
    # notify(f"Balance after trading : {krw}")
    print(f"$ Balance after trading : {krw}")
    print("--- %s seconds ---" % (time.time() - start_time))
    return krw


krw = 35000
i = 0
start_time = time.time()
while time.time() - start_time < 3600:
    krw = upbit_triangular_roundtrip(krw)
    i += 1 

