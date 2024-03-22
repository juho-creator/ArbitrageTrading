[![English](https://img.shields.io/badge/lang-English-blue.svg)](https://github.com/juho-creator/triangular_arbitrage/blob/main/README.md)
[![한국어](https://img.shields.io/badge/lang-한국어-red.svg)](https://github.com/juho-creator/triangular_arbitrage/blob/main/README.KR.md)

# Triangular Arbitrage Trading

> [!CAUTION]  
> **This study focuses solely on the Upbit exchange until February 21st, 2024 </br>
>  Conditions on other exchanges are not considered</br>
> CONTENT IS SUBJECT TO CHANGE AFTER UPDATES**

> [!NOTE]
> **Code is not shared as it's still under development.**

![306502733-a9c56335-69fd-4df9-9e00-2a9b42946890](https://github.com/juho-creator/triangular_arbitrage/assets/72856990/cfe964f7-e0d6-404d-8cfa-3409926ee38f)


- Triangular Arbitrage trading aims to profit from arbitrage opportunities among different crypto pair markets
- Trading can occur clockwise or anticlockwise depending on the available arbitrage opportunities
- Upbit Exchange offers two types of crypto markets: BTC and KRW
- Out of 119 cryptos registered on Upbit, only 98 support the BTC market


</br>


## Greatest Challenge
> [!NOTE]
> **This section highlights the challenges encountered when executing triangular arbitrage trading. </br>
> For more detailed information, please refer to the accompanying [notes](https://github.com/juho-creator/triangular_arbitrage/blob/main/triangular_arbitrage.pdf).**


### Trading Levels
Trading levels categorize orders based on their complexity, with Level 3 representing the most intricate orders. </br>
Profit and execution speed vary depending on the trading level. 
Let's examine the execution of the **oneway()** function at each trading level:
</br></br>

#### &nbsp; Level 1 (Market Order) 
 Three **instant** market orders are executed at market prices, buying at ask prices and selling at bid prices for immediate execution. </br>
 However, this often results in **slippage** (buying high, selling low), leading to a guaranteed loss.
</br></br>

#### &nbsp; Level 2 (BUY low, SELL high)
At Level 2, limit orders are placed at bid/ask prices to seize arbitrage opportunities. However, there's no guarantee of fulfillment, leading to potential delays and missed opportunities within the trading loop.
</br></br>

#### &nbsp;Level 3 (BUY high, SELL low)
Level 3 entails placing instant limit buy/sell orders at ask/bid prices. While this guarantees instant execution, it reduces arbitrage opportunities and makes profiting from small opportunities challenging.
</br></br>

Trading at Level 3 is considered optimal for profit, although identifying arbitrage opportunities surpassing transaction fees poses a challenge. Furthermore, market volatility may result in the disappearance of desired price levels, thereby complicating the process of exiting the trading loop.
</br></br></br>


### Inherently illiquid BTC pair market
Due to lower trading activity compared to KRW pair markets, BTC pair markets exhibit extremely low trading volumes, resulting in significant spreads between bid and ask prices. This often leads to unfilled orders or slippage when placing orders in the BTC pair market. Paradoxically, this illiquidity also creates disparities between the spreads of KRW and BTC pair markets, [offering arbitrage opportunities](https://www.youtube.com/clip/UgkxjqQU0dMrhLZH7qmjGzrWW1lKQGeSzllp).</br>

To ensure successful execution of Level 3 trading, available quantities at all three price levels must exceed our trading balance. However, spotting arbitrage opportunities that outweigh transaction fees at price levels with sufficient volumes becomes increasingly challenging. Nevertheless, such detection significantly enhances the probability of successful trading.
</br>
</br>


## Current Progress 
Due to market illiquidity, various challenges arose while placing orders. Here's a summary of the efforts made to improve the algorithm and the encountered issues during development:

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
- [X] Cancel triangular arbitrage if first limit order takes more than 20seconds
- [ ] Only monitor a high volume, volatile crypto currency (close analysis on trade)
- [ ] Add Telegram API
</br></br>




## Technology used
- **main.py** : Arbitrage Trading Strategies
  - Spatial arbitrage (Transferring between exchanges)
  - Spatial arbitrage  (No transferring between exchanges)
  - Triangular arbitrage
  
- **modules.py** : Functions used in Arbitrage Trading Algorithms
- **bot.py** : Telegram API for UI
</br>
</br>

## Using Chatgpt 
</br>

#### Setting Custom Instructions
![image](https://github.com/juho-creator/triangular_arbitrage/assets/72856990/c99bd5b8-c105-4788-b685-a4f78360dd50)
</br></br>


The custom instruction above for GPT was set in advance to:
- Provide concise responses with relevant information.
- Avoid unnecessary details for clarity.
</br>


## Reference
**Code**
- [Upbit API documentation](https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EA%B3%84%EC%A2%8C-%EC%A1%B0%ED%9A%8C)
- [pyupbit documentation](https://github.com/sharebook-kr/pyupbit?tab=readme-ov-file)
- [Bithumb API documentation](https://apidocs.bithumb.com/reference/%ED%98%B8%EA%B0%80-%EC%A0%95%EB%B3%B4-%EC%A1%B0%ED%9A%8C)
- [Binance API documentation](https://binance-docs.github.io/apidocs/spot/en/)
- [CCXT API documentation](https://docs.ccxt.com)
-	[Binance C++ API](https://github.com/binance-exchange/binacpp)
- [Use case of Telegram API](https://charliethewanderer.medium.com/scrape-news-and-corporate-announcements-in-real-time-2-deployment-27ae489f598a)
- [Benchmarking in Python](https://www.youtube.com/watch?v=DBoobQxqiQw)
</br>
 
  
**Trading Concepts**
- [Crypto Arbitrage Trade Guide](https://coincodecap.com/crypto-arbitrage-guide-how-to-make-money-as-a-beginner)
- [Arbitrage trading with Kimchi premium](https://charlietrip.tistory.com/19)
- [Triangular Arbitrage](https://www.youtube.com/watch?v=lKu2LAgEcpU)
- [Why Triangular Arbitrage Works](https://www.youtube.com/clip/UgkxjqQU0dMrhLZH7qmjGzrWW1lKQGeSzllp)
- [What is Slippage?](https://www.youtube.com/watch?v=gaVYPGrxykw)
- [Understanding Orderbooks](https://www.youtube.com/watch?v=Jxyuf-cDKeg)
- [Who Decides the Prices of Stocks?](https://www.youtube.com/watch?v=HxNH7xi4zq8)
- [Reading in Depth Chart](https://youtube.com/clip/Ugkx0c5M3OF96EjkuDo8IfXJGjiR6XCdZ8_f?si=jnnrMETCA_Mn0iLC)
- [Trader's Mindset](https://www.youtube.com/clip/Ugkx2DdNUkPZUtbCsDDo0xmG4veFGHboxH49)
</br>


**Regulations**
- [트래블룰이란?](https://upbitcs.zendesk.com/hc/ko/articles/4498679629337-%ED%8A%B8%EB%9E%98%EB%B8%94%EB%A3%B0-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0)
- [Is kimchi premium illegal?](https://youtube.com/shorts/YF3FK_4NOmM?si=ZgVCQ__LfEPyzb97)
</br>

**Upbit Exchange**
- [유의 종목과 주의 종목](https://upbitcs.zendesk.com/hc/ko/articles/900005994766-%EC%9C%A0%EC%9D%98-%EC%A2%85%EB%AA%A9%EA%B3%BC-%EC%A3%BC%EC%9D%98-%EC%A2%85%EB%AA%A9%EC%9D%B4-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%EC%9A%94)
- [거래 이용 안내](https://upbitcs.zendesk.com/hc/ko/articles/4403838454809-%EA%B1%B0%EB%9E%98-%EC%9D%B4%EC%9A%A9-%EC%95%88%EB%82%B4)


