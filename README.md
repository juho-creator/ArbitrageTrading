# Arbitrage Trading 
## Motivation
Think about what you really want in life.
Do you want to wake up every day worrying about your personal finance?
Living with a person I hate dreadfully?
Not having a single passionate person to talk to?
Always living under standards set by other people?
Where does that even lead to?
NO WHERE!!!

So you are going to figure it out.
It's going to be a long journey but I know you will figure it out.
You might have to struggle alot.
But you know it's worth it
Every attempt you've failed will all make sense and guide you. 

DO NOT EVER GIVE UP.

여기 살면서 덕분에 대다수가 평생 느낄수 없는 경험을 했다.
난 그래도 절때 갑과 을 관계로 항상 쩔쩔 기면서 ㅈ같이 살고 싶지 않다.
점점 그렇게 되가고 자연스럽게 그게 맞다고 생각한 사고방식이 진짜 싫다.
이 느낌 잊지마.
자기 자신이 걍 보스라 생각하고 걍 지 멋대로
자신이 생각하는 가치관 아래서 계속 평가 당하는 이 찝찝하고 더러운 기분.

자신의 가치관과 신념 항상 강조하고 막상 상대 생각은 없는 정말 징그러운 사람.
넌 그래서 너만의 방식을 찾아야되.    
다른 사람이 강조하는 방식으로 살면
너 자신을 잃게되는거야
오늘 진짜 그거 하나 잘 배웠다



# Current Progress 
Due to illiquid market, I faced several issues on orders.
Following attempts of Triangular Arbitrage were executed on Upbit:
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
- [ ] Only monitor a high volume, volatile crypto currency (close analysis on trade)
- [ ] Implement order reminders (More time to work on something else while testing)


## Greatest Challenge
### order speed & order profit tradeoff
For faster limit order fills, buy/sell orders were implemented at ask/bid prices respectively. 
However, the since we are buying high and selling low, arbitrage opportunities are not detected.

Since the only illiquid market is BTC_CODE, we could buy/sell at ask/bid and try buy/sell orders at bid/sell on KRW_CODE and KRW_BTC 
for spotting arbitrage opporunities.
Problem with this is that we are able to find the opportunities, but it's not guaranteed that order would be filled in volatile markets.

**Solution :**  </br>
- [ ] Try buy/sell orders at bid/ask price on KRW_CODE and KRW_BTC on liquid market and  buy/sell at ask/bid price for faster execution
- [ ]  KRW_CODE and KRW_BTC at market price
- [ ] Less volatile crypto






</br>
Following attempts of Triangular Arbitrage were executed on Binance: 
- [ ] 

</br>
Following attempts of Triangular Arbitrage were executed on Bithumb: 
- [ ] 


</br>
Following attempts of spatial arbitrage were executed on Bithumb and Binance 
- [ ] 







# Life Goals 
### After earning $100k
- [ ] Hosting $10K family trip to a wonderful place for healing
- [ ] Get new electronic devices
- [ ] Buy new clothes
</br> **RECREATE REPOSITORY WITH CODE ENCRYPTED WITH KLEOPATRA**
</br>

### After earning $1M
- [ ] Living in suburban area
- [ ] Starting a business with chong chong

</br>

### After earning $10M
- [ ] Buying a house in California
</br>
</br>



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

