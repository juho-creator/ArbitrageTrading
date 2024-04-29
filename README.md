[![English](https://img.shields.io/badge/lang-English-blue.svg)](https://github.com/juho-creator/ArbitrageTrading/blob/main/README.md)
[![한국어](https://img.shields.io/badge/lang-한국어-red.svg)](https://github.com/juho-creator/ArbitrageTrading/blob/main/README.KR.md)

# Triangular Arbitrage trading 
 > [!CAUTION]  
>**This is a study soley performed on Upbit exchange until 21st Feburary 2024. </br>
Conditions that may appear on other exchanges is not reflected in this README. </br>
ANY CONTENT IS SUBJECT TO CHANGE AFTER UPDATE**

> [!NOTE]
>**Code is not shared as it's still under development**
</br></br>

![image](https://github.com/juho-creator/ArbitrageTrading/assets/72856990/a9c56335-69fd-4df9-9e00-2a9b42946890)

- Triangular Arbitrage trading seeks to profit by taking arbitrage opportunities among different crypto pairs. </br>
- Trading can take place in both clockwise and anticlockwise direction depending on the available arbitrage opportunity as shown on the diagram above.
- There are 2 types of crypto market at Upbit Exchange. (BTC and KRW)
- Out of 119 cryptos registered in the Upbit exchange, only 98 support BTC market. 


</br></br>

# Understanding the authentication process of UPBIT API
### Creating the JWT token
![image](https://github.com/juho-creator/ArbitrageTrading/assets/72856990/a6eed351-f526-4a01-ad82-fd63d1cff341)
</br></br>

### SHA512 vs SHA256
![image](https://github.com/juho-creator/ArbitrageTrading/assets/72856990/3ef53251-8b98-4632-8f2e-963df54ca448)
</br></br>


### Base64URL vs Base64 encoding
![image](https://github.com/juho-creator/ArbitrageTrading/assets/72856990/9171fffb-81d8-486f-b9d7-040f9576843b)
</br></br>

### FOK vs IOC 
![image](https://github.com/juho-creator/ArbitrageTrading/assets/72856990/1a64c1fd-b72a-4f6c-903b-9ce34891d648)
</br>
삼각차익거래엔 FOK를 활용해야 확실한 주문가능
</br></br>





## Current Progress 
Due to illiquid market, I faced several issues on placing orders. </br>
Following are attempts that were/to be made to improve the algorithm along with the issues that arose after development : 
- [x] Create Market Orders (create fast orders)
   - **slippage**
- [X] Create Limit Order (prevent slippage)
   - **Order waiting to be filled at desired price**
- [X] Buy/Sell Limit orders each set to ask/bid for instant order (fast order at desired price)
   - **Orders partially filled due to insufficient volume at bid/prices**
   - **Sudden price change created gap between market price and order price**
- [X] Optimize code and eliminate unnecessary API calls (improve runtime)
- [X] Take minimum BTC = 0.005 into consideration before performing trade (prevent entry at illiquid price)
- [X] Organize the code as a package (for code maintenance)
- [X] Reduce API call for limit order (improve runtime) 
- [X] Create order when profit >= 0.35% (secure profitable trade)
- [X] Increase speed for spotting arbitrage opportunities (spot arbitrage opportunity quickly) 
- [X] Adjust bid/ask price level (change sensitivity of order execution)
  - **Buy high and sell low --> arbitrage not detected**
- [X] Double check if limit/market orders work in both directions
- [X]  Cancel limit order if it's on hold for more than 20 units
- [X]  Check quantity before executing arbitrage
   - **OneWay : BTC-CODE, KRW-BTC**
   - **OtherWay : BTC-CODE, KRW-CODE**
- [X] Implement order reminders (More time to work on something else while testing)
- [ ] Only monitor a high volume, volatile crypto currency (close analysis on trade)
- [ ] Add Telegram API
</br>

## Greatest Challenge

### Profitable Order Guarantee & Arbitrage Opportunity Tradeoff

The relation betweeen profitable order guarantee and order speed is inversely proportional.</br>
Increasing guaranteed profitable orders decreases arbitrage opportunities, while increasing order speed has the opposite effect. </br>
This occurs because attempting to buy high and sell low reduces the arbitrage gap while ensuring order fills.</br>

Let's take the execution of **oneway()** at different levels for reference:

**Level 1 (Market Order):**
Orders are placed at market prices, offering ask prices when buying and bid prices when selling for instant orders. This leads to buying high, selling low, and then selling low again, resulting in slippage and a guaranteed losing triangular arbitrage trade.

**Level 2 (BUY low, SELL high):**
While seemingly ideal for maximizing arbitrage opportunities at exact price levels, there's no guarantee of orders being filled. Orders may remain unfilled, and even if filled, there's no assurance of subsequent orders being filled. In practice, it's nearly impossible for all orders to be filled as desired.

**Level 3 (BUY high, SELL low):**
Orders are placed when buyers and sellers exist at the desired price, almost guaranteeing execution. However, it becomes challenging to profit from small arbitrage opportunities.

This concise overview highlights the tradeoff between ensuring profitable orders and maximizing arbitrage opportunities. For more information, please refer to my notes.

### Inherently illiquid BTC pair market

**Solution :**  </br>
- [ ] Try buy/sell orders at bid/ask price on KRW_CODE and KRW_BTC on liquid market and  buy/sell at ask/bid price for faster execution
- [ ]  KRW_CODE and KRW_BTC at market price
- [ ] Less volatile crypto


Unable to find/execute triangular arbitrage (ISSSUE WITH DEMAND & SUPPLY)
- Too much gap between bid/ask of BTC_CODE market
- Hence, BTC_CODE is. Bought/sold.at overprice/.underprice
- Order price at BTC_CODE must be fixed to make quick entry/exits in illiquid market
- Adjusting price levels for KRW_CODE & KRW_BTC helped identify arbitrage opportunities
- However, the likelihood of the order taking place below 10 price levels is very unlikely
- Even though I’m able to detect the arbitrage opportunity from the orderbook, it’s not executed because buyers and sellers are not coming to an agreement to my price
- But if I were to change the logic to buy at ask price and sell at bid price (buy high, sell low) the order is guaranteed to be executed. However, it becomes increasingly difficult to find arbitrage opportunities



Code update
 - Cancel triangular arbitrage if limit order takes more than 20seconds
- Ran my code at .venv








</br>
Following attempts of Triangular Arbitrage were executed on Binance: 
- [ ] 

</br>
Following attempts of Triangular Arbitrage were executed on Bithumb: 
- [ ] 


</br>
Following attempts of spatial arbitrage were executed on Bithumb and Binance 
- [ ] 





## Technology used
- **main.py** : Arbitrage Trading Strategies
  - Spatial arbitrage (Transferring between exchanges)
  - Spatial arbitrage  (No transferring between exchanges)
  - Triangular arbitrage
  
- **modules.py** : Functions used in Arbitrage Trading Algorithms
- **bot.py** : Telegram API for UI

## Reference
**Code**
- [Upbit API documentation](https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EA%B3%84%EC%A2%8C-%EC%A1%B0%ED%9A%8C)
- [pyupbit documentation](https://github.com/sharebook-kr/pyupbit?tab=readme-ov-file)
- [Binance API documentation](https://binance-docs.github.io/apidocs/spot/en/)
- [CCXT API documentation](https://docs.ccxt.com)
-	 [Binance C++ API](https://github.com/binance-exchange/binacpp)
- [Use case of Telegram API](https://charliethewanderer.medium.com/scrape-news-and-corporate-announcements-in-real-time-2-deployment-27ae489f598a)
- [Benchmarking in Python](https://www.youtube.com/watch?v=DBoobQxqiQw)

**Technical concepts**
- [Test SHA512](https://emn178.github.io/online-tools/sha512.html)
- [Test SHA256](https://emn178.github.io/online-tools/sha256.html)
- [Test Base64URL](https://base64.guru/standards/base64url/encode)
- [Test Base64](https://www.base64encode.org/)
  
**Trading Concepts**
- [Crypto Arbitrage Trade Guide](https://coincodecap.com/crypto-arbitrage-guide-how-to-make-money-as-a-beginner)
- [김프거래 가이드](https://charlietrip.tistory.com/19)
- 
- [Triangular Arbitrage](https://www.youtube.com/watch?v=lKu2LAgEcpU)
- [Why Triangular Arbitrage Works](https://www.youtube.com/clip/UgkxjqQU0dMrhLZH7qmjGzrWW1lKQGeSzllp)
-
- [What is Slippage?](https://www.youtube.com/watch?v=gaVYPGrxykw)
- [Understanding Orderbooks](https://www.youtube.com/watch?v=Jxyuf-cDKeg)
- [Who Decides the Prices of Stocks?](https://www.youtube.com/watch?v=HxNH7xi4zq8)
- [Reading in Depth Chart](https://youtube.com/clip/Ugkx0c5M3OF96EjkuDo8IfXJGjiR6XCdZ8_f?si=jnnrMETCA_Mn0iLC)


**Regulations**
- [트래블룰](https://upbitcs.zendesk.com/hc/ko/articles/4498679629337-%ED%8A%B8%EB%9E%98%EB%B8%94%EB%A3%B0-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0)
- [김프차익거래 불법인가?](https://youtube.com/shorts/YF3FK_4NOmM?si=ZgVCQ__LfEPyzb97)

