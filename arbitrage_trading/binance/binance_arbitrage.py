def binanceTriangular(code):
    USDT_CODE = binance_price(f"{code}USDT")
    BTC_CODE = binance_price(f"{code}BTC")
    USDT_BTC = binance_price("BTCKRW")

    print(f"KRW-{code} : " + str(USDT_CODE))
    print(f"BTC-{code} : " + str(BTC_CODE))
    print("KRW-BTC : " + str(USDT_BTC))

    KRW_NEW_CODE = round(BTC_CODE * USDT_BTC, 2)

    if USDT_CODE < KRW_NEW_CODE:
        print(f"KRW-{code} ==> BTC-{code} ==> KRW-BTC")
        profit = round((KRW_NEW_CODE - USDT_CODE) / USDT_CODE * 100, 2)
        print(f"{USDT_CODE} ==> {KRW_NEW_CODE} ({profit}%)")
        return True, profit, USDT_CODE, BTC_CODE, USDT_BTC
    else:
        print(f"KRW-BTC ==> BTC-{code} ==> KRW-{code}")
        profit = round((USDT_CODE - KRW_NEW_CODE) / KRW_NEW_CODE * 100, 2)
        print(f"{KRW_NEW_CODE} ==> {USDT_CODE} ({profit}%)")
        return False, profit, USDT_CODE, BTC_CODE, USDT_BTC


