from arbitrage_trading import *
import time

from elevenlabs import generate, play

audio = generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice= "Sarah",
  model="eleven_multilingual_v2"
)

play(audio)

# start_time = time.time()

# for crypto in available_cryptos:
#     upbit_triangular(crypto)


# print("--- %s seconds ---" % (time.time() - start_time))

