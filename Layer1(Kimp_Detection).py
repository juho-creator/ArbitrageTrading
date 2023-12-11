import asyncio
import websockets
import json

async def binance_worker(ws, msg):
    await ws.send(msg)
    while True:
        data = await ws.recv()
        print("Binance:")
        print(json.loads(data))

async def upbit_worker(ws, msg):
    await ws.send(msg)
    while True:
        data = await ws.recv()
        print("Upbit:")
        print(json.loads(data))

async def run():
    binance_url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    upbit_url = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(binance_url) as binance_ws, websockets.connect(upbit_url) as upbit_ws:
        binance_subscribe_msg = json.dumps({
            "method": "SUBSCRIBE",
            "params": {"streams": ["btcusdt@kline_1m"]}
        })
        upbit_subscribe_msg = json.dumps([
            {"ticket": "test"},
            {"type": "ticker", "codes": ["KRW-BTC"]}
        ])

        await asyncio.gather(
            binance_worker(binance_ws, binance_url),
            upbit_worker(upbit_ws, upbit_subscribe_msg)
        )

asyncio.run(run())
