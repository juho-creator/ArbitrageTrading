import asyncio
import websockets
import json
from pprint import pprint


async def binance_websocket(symbol):
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}usdt@kline_1m"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            parsed_response = json.loads(response)
            binance_close = float(parsed_response["k"]["c"])
            print(f"Binance Close Price ({symbol}): {binance_close}")
            return binance_close


async def upbit_websocket(symbol):
    uri = "wss://api.upbit.com/websocket/v1"
    payload = [{"ticket": "test"}, {"type": "ticker", "codes": [f"KRW-{symbol}"], "isOnlyRealtime": True}]

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(payload))

        while True:
            response = await websocket.recv()
            parsed_response = json.loads(response)
            upbit_close = parsed_response["trade_price"]
            print(f"Upbit Close Price ({symbol}): {upbit_close}")
            return upbit_close


async def main():
    symbol = "EOS"
    currency = 1319.4

    upbit_close = await upbit_websocket(symbol)
    binance_close = await binance_websocket(symbol)

    calculated_value = ((upbit_close / (binance_close * currency)) - 1) * 100
    print(f"Calculated Value: {calculated_value}")


    if  calculated_value>0:
        print("김프")
    else:

        print("역프")


asyncio.run(main())
