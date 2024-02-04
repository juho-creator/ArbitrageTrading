from arbitrage_trading import *
import time
import pyttsx3




# engine = pyttsx3.init()
# engine.say("Triangular Arbitrage completed")
# engine.runAndWait()


start_time = time.time()

# cryptos = available_cryptos
# for crypto in cryptos:
#     upbit_triangular(crypto)

upbit_triangular("XTZ")


print("--- %s seconds ---" % (time.time() - start_time))

