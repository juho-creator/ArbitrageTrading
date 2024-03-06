import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import pyupbit
import math
from ..config import ACCESS_KEY,SECRET_KEY
import pandas as pd
import sys
from ..binance.binance_user import BinanceAddress
from .upbit_module import notify

UPBIT_TICKERS = [
    "BTC",
    "ETH",
    "NEO",
    "MTL",
    "XRP",
    "ETC",
    "SNT",
    "WAVES",
    "XEM",
    "QTUM",
    "LSK",
    "STEEM",
    "XLM",
    "ARDR",
    "ARK",
    "STORJ",
    "GRS",
    "ADA",
    "SBD",
    "POWR",
    "BTG",
    "ICX",
    "EOS",
    "TRX",
    "SC",
    "ONT",
    "ZIL",
    "POLYX",
    "ZRX",
    "LOOM",
    "BCH",
    "BAT",
    "IOST",
    "CVC",
    "IQ",
    "IOTA",
    "HIFI",
    "ONG",
    "GAS",
    "UPP",
    "ELF",
    "KNC",
    "BSV",
    "THETA",
    "QKC",
    "BTT",
    "MOC",
    "TFUEL",
    "MANA",
    "ANKR",
    "AERGO",
    "ATOM",
    "TT",
    "CRE",
    "MBL",
    "WAXP",
    "HBAR",
    "MED",
    "MLK",
    "STPT",
    "ORBS",
    "VET",
    "CHZ",
    "STMX",
    "DKA",
    "HIVE",
    "KAVA",
    "AHT",
    "LINK",
    "XTZ",
    "BORA",
    "JST",
    "CRO",
    "TON",
    "SXP",
    "HUNT",
    "PLA",
    "DOT",
    "MVL",
    "STRAX",
    "AQT",
    "GLM",
    "SSX",
    "META",
    "FCT2",
    "CBK",
    "SAND",
    "HPO",
    "DOGE",
    "STRK",
    "PUNDIX",
    "FLOW",
    "AXS",
    "STX",
    "XEC",
    "SOL",
    "MATIC",
    "AAVE",
    "1INCH",
    "ALGO",
    "NEAR",
    "AVAX",
    "T",
    "CELO",
    "GMT",
    "APT",
    "SHIB",
    "MASK",
    "ARB",
    "EGLD",
    "SUI",
    "GRT",
    "BLUR",
    "IMX",
    "SEI",
    "MINA",
    "CTC",
    "ASTR",
]

# API Authentication 
upbit = pyupbit.Upbit(ACCESS_KEY,SECRET_KEY)


# Checking Balance
def krw_balance():
    KRW = upbit.get_balance("KRW")
    # print(f"KRW balance : {KRW}")
    try:
        KRW_AVAILABLE = "{:.6f}".format(KRW * 0.995)
        print(f"Available KRW balance : {KRW_AVAILABLE}\n")
        return float(KRW_AVAILABLE)
    except TypeError:
        raise SystemExit("IP not registered in UPBIT")

def crypto_balance(symbol, transaction_fee=0):
    try:
        crypto_quantity = upbit.get_balance(symbol) - transaction_fee

        print(f"\n{symbol} balance: {crypto_quantity:.8f} (Upbit)")
        return crypto_quantity
    except:
        print(f"Unable to retrieve {symbol} balance (Upbit)")


# Placing Orders
def upbit_buy(symbol, volume):
    try:
        print(f"\nBuying {symbol} at UPBIT")
        upbit_buy = upbit.buy_market_order(f"{symbol}", volume)
        print(upbit_buy)  # 주문내역
        order_id = upbit_buy["uuid"]  # 주문번호 저장
        order_state = upbit.get_individual_order(order_id)["state"]

        # Wait until order is filled
        while order_state not in ["cancel", "done"]:
            print("Market Buy Order Taking place...")
            order_state = upbit.get_individual_order(order_id)["state"]
        executed_volume = upbit.get_individual_order(order_id)["executed_volume"]
        return float(executed_volume)
    except Exception as e:
        print(f"Unable to buy {symbol} (Upbit)")
        print(e)

def upbit_sell(symbol, volume):
    try:
        print(f"Selling {symbol} at UPBIT")
        upbit_sell = upbit.sell_market_order(f"{symbol}", volume)
        print(upbit_sell)
        order_id = upbit_sell["uuid"]  # 주문번호 저장
        order_state = upbit.get_individual_order(order_id)["state"]

        # Wait until order is filled
        while order_state not in ["cancel", "done"]:
            print("Market Sell Order Taking place...")
            order_state = upbit.get_individual_order(order_id)["state"]
        executed_volume = upbit.get_individual_order(order_id)["executed_volume"]
        return float(executed_volume)

    except Exception as e:
        print(f"Unable to sell {symbol} (Upbit)")
        print(e)

def upbit_limit_buy(symbol, price, volume):
    try:
        print(f"\nBuying {symbol} at UPBIT")
        upbit_buy = upbit.buy_limit_order(f"{symbol}", price, volume)
        print(upbit_buy)  # 주문내역
        order_id = upbit_buy["uuid"]  # 주문번호 저장
        order_state = upbit.get_individual_order(order_id)["state"]
        
        # Wait until order is filled
        wait = 1
        while order_state not in ["cancel", "done"]:
            if wait == 1:
                notify("Entering cancel countdown")

            if wait == 20:
                cancel_result = upbit.cancel_order(order_id)
                print(cancel_result)
                sys.exit()
            print(f"Limit Buy Order Taking place... {wait}")
            order_state = upbit.get_individual_order(order_id)["state"]
            wait += 1
        return float(upbit_buy["volume"])
    except Exception as e:
        print(f"Unable to buy {symbol} (Upbit)")
        print(e)

def upbit_limit_sell(symbol, price, volume):
    try:
        print(f"Selling {symbol} at UPBIT")
        upbit_sell = upbit.sell_limit_order(f"{symbol}", price, volume)
        print(upbit_sell)
        order_id = upbit_sell["uuid"]  # 주문번호 저장
        order_state = upbit.get_individual_order(order_id)["state"]

        # Wait until order is filled
        wait = 1
        while order_state not in ["cancel", "done"]:
            if wait == 1:
                notify("Entering cancel countdown")
                
            if wait == 20:
                cancel_result = upbit.cancel_order(order_id)
                print(cancel_result)
                sys.exit()
            print(f"Limit Sell Order Taking place... {wait}")
            order_state = upbit.get_individual_order(order_id)["state"]
            wait += 1
        return float(upbit_sell["volume"])

    except Exception as e:
        print(f"Unable to sell {symbol} (Upbit)")
        print(e)


# Withdraw/Deposit
def UpbitAddress(symbol):
    try:
        wallet = upbit.get_individual_deposit_address(symbol, symbol)
        address = wallet["deposit_address"]
        tag = wallet["secondary_address"]
        return address, tag
    except:
        print(f"{symbol} wallet not found")

def UpbitWithDraw(symbol, CRYPTO_AVAILABLE):
    try:
        print(f"\nWithdrawing {symbol} (UPBIT -> Binance)")
        address, tag = BinanceAddress(symbol)
        upbit_send = upbit.withdraw_coin(symbol, symbol, CRYPTO_AVAILABLE, address, tag)
        pprint(upbit_send)
        transaction_id = upbit_send["uuid"]

        transaction_state = upbit.get_individual_withdraw_order(transaction_id, symbol)[
            "state"
        ]
        while transaction_state != "DONE":
            print(f"Transfering {symbol}.... (UPBIT --> Binance)")
            try:
                transaction_state = upbit.get_individual_withdraw_order(
                    transaction_id, symbol
                )["state"]
            except Exception as e:
                print(e)
        print("Successfully sent to Binance")

        return transaction_id, transaction_state
    except:
        print(f"Unable to withdraw {symbol} from Upbit")

def UpbitRECEIVED(txid, symbol, quantity):
    deposit_state = "None"

    while deposit_state != "ACCEPTED":
        try:
            deposit_state = upbit.get_individual_deposit_order(txid, symbol)["state"]
            pprint(deposit_state)
            print("Confirming at UPBIT...")
        except:
            print("Waiting at UPBIT...")
    print("Received at UPBIT!")
    UPBIT_CRYPTO = crypto_balance(symbol)
    while UPBIT_CRYPTO < quantity:
        print("Waiting for UPBIT balance to be updated")
        UPBIT_CRYPTO = crypto_balance(symbol)

    return UPBIT_CRYPTO


