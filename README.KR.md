[![영어](https://img.shields.io/badge/lang-영어-blue.svg)](https://github.com/juho-creator/ArbitrageTrading/blob/main/README.md)
[![한국어](https://img.shields.io/badge/lang-한국어-red.svg)](https://github.com/juho-creator/ArbitrageTrading/blob/main/README.KR.md)

# 삼각차익거래

> [!주의]  
> **이 공부는 2024년 2월 21일까지 진행됬고 업비트 거래소에만 중점을 두고 있습니다.</br>
> 다른 거래소의 조건은 고려되지 않았습니다.</br>
> 내용은 언제든 수정될 수 있습니다.**

> [!참고]
> **코드는 아직 개발 중이므로 공유되지 않았습니다.**

![이미지](https://github.com/juho-creator/ArbitrageTrading/assets/72856990/a9c56335-69fd-4df9-9e00-2a9b42946890)

- 삼각차익거래는 서로 다른 암호 화폐 페어 시장 사이의 차익 거래 기회에서 이익을 얻으려는 것을 목표로 합니다.
- 거래는 이용 가능한 차익 거래 기회에 따라 시계 방향 또는 반시계 방향으로 발생할 수 있습니다.
- 업비트 거래소는 BTC 및 KRW 두 가지 유형의 암호 화폐 시장을 제공합니다.
- 업비트에 등록된 119개의 암호 화폐 중 98개만 BTC 시장을 지원합니다.


</br>


## 제일 어려웠던 문제
> [!참고]
> **이 간략한 개요는 수익성 있는 주문 보장과 차익 거래 기회 극대화 사이의 절충 관계를 강조합니다. </br>
> 자세한 정보는 제 노트를 참고해주세요.**
### 수익성 주문 보장 & 차익 거래 기회

수익성 주문 보장과 주문 속도 사이의 관계는 반비례적입니다.</br>
보장된 수익성 주문이 증가함에 따라 차익 거래 기회는 감소하고 그 반대도 마찬가지입니다.</br> 
이는 높게 매입하여 낮게 매도함으로써 차익 갭을 줄이면서 주문 채움을 보장하기 때문에 발생합니다.</br>
</br>
참고용으로 **oneway()**의 실행을 다른 레벨에서 살펴보겠습니다:
</br>
#### 레벨 1 (시장 주문) 
 시장 가격에서 세 개의 즉시 시장 주문이 실행되며, 즉시 실행을 위해 매도가격에 매입하고 매입 가격에 매도합니다. 그러나 이로 인해 종종 높게 매입하고 낮게 매도하며 슬리피지를 발생시키므로, 보장된 삼각 화폐 차익 거래는 손실이 보장됩니다.

#### 레벨 2 (낮게 매입, 높게 매도)
세 개의 한정 매수/매도 주문이 매도/매수 가격에 설정되어, 정확한 가격 지점에서 차익 거래 기회를 활용하고자 합니다. 그러나 주문 채움의 확실성은 없으며, 실제로 의도한 대로 모든 세 개의 주문이 채워지는 것은 매우 불가능합니다.

#### 레벨 3 (높게 매입, 낮게 매도)
세 개의 한정 매수/매도 주문이 매도/매수 가격에 위치하여, 구매자와 판매자가 의도한 가격에서 일치할 때 실행됩니다. 이는 실행을 거의 보장하지만, 작은 차익 거래 기회에서 수익을 얻는 것이 어려워집니다.


</br></br>

### 본질적으로 비액화된 BTC 페어 시장
KRW 페어 시장과 비교하여 거래 활동이 적은 BTC 페어 시장은 매도 및 매수 가격 간의 큰 차이로 인해 거래량이 극도로 낮습니다. 이로 인해 실행 중에 주문이 채워지지 않거나 슬리피지가 발생하는 경우가 많습니다. 역설적으로, 이 비액화성은 KRW와 BTC 페어 시장 간의 차이를 만들어내어 차익 거래 기회를 제공합니다.


따라서 수익성 있는 주문 실행과 주문 속도 사이의 균형을 유지하는 것이 성공적인 삼각 화폐 거래를 달성하기 위해 필요합니다. 시장 주문은 종종 슬리피지를 초래하며, 매수/매도 가격에 한정 주문은 주문이 채워지지 않을 수 있으며, 이로 인해 삼각 화폐 거래 과정이 지연될 수 있습니다.

매수/매도 가격에 한정 주문을 배치하면 가장 수익성 있는 주문 보장과 즉각적인 실행 속도를 제공합니다. 높게 매입하여 낮게 매도함으로써 차익 거래 기회를 줄이지만, 이 방법은 원하는 가격 수준에서 즉각적인 주문을 용이하게 합니다.
</br>
</br>


## 현재 진행 상황 
시장의 유동성이 낮아 주문을 배치할 때 많은 도전에 직면했습니다. 다음은 알고리즘을 개선하고 개발 중에 발생한 문제를 해결하기 위해 시도한 내용입니다:
- [x] 시장 주문 생성 (빠른 주문 생성)
   - **슬리피지**
- [X] 한정 주문 생성 (슬리피지 방지)
   - **원하는 가격에 주문 채워질 대기중**
- [X] 매수/매도 한정 주문 각각을 즉각 주문을 위해 매도/매수로 설정 (원하는 가격에 빠른 주문)
   - **입찰/매도 가격에서 부족한 볼륨으로 주문 일부가 채워짐**
   - **급격한 가격 변동으로 시장 가격과 주문 가격 사이의 차이가 발생**
- [X] 코드 최적화 및 불필요한 API 호출 제거 (런타임 개선)
- [X] 거래 전에 최소 BTC = 0.005를 고려 (비액화 가격에 대한 진입 방지)
- [X] 코드를 패키지로 구성 (코드 유지 관리를 위해)
- [X] 한정 주문을 위한 API 호출 감소 (런타임 개선) 
- [X] 수익률이 0.35% 이상인 경우 주문 생성 (수익성 있는 거래 보장)
- [X] 차익 기회 신속히 발견하는 속도 증가 (차익 기회 신속 발견)
- [X] 입찰/매도 가격 수준 조정 (주문 실행의 민감도 조정)
  - **높게 매입하고 낮게 매도함 --> 차익 감지되지 않음**
- [X] 한정/시장 주문이 양방향으로 작동하는지 두 번 확인
- [X] 20 단위 이상 대기 중인 한정 주문 취소
- [X] 삼각 화폐 거래를 실행하기 전에 수량을 확인
   - **원웨이: BTC-CODE, KRW-BTC**
   - **다른 방법: BTC-CODE, KRW-CODE**
- [X] 주문 알림 구현 (테스트 중에 다른 작업을 수행하는 데 더 많은 시간 확보)
- [X] 첫 번째 한정 주문이 20초 이상 소요되면 삼각 화폐 거래 취소
- [ ] 고액, 변동성이 높은 암호 화폐만 모니터링
- [ ] 텔레그램 API 추가
</br></br>




## 사용된 기술
- **main.py** : 차익 거래 전략
  - 공간적 차익 (거래소 간 이전)
  - 공간적 차익 (거래소 간 이전 없음)
  - 삼각차익거래
  
- **modules.py** : 차익 거래 알고리즘에 사용된 함수
- **bot.py** : UI를 위한 텔레그램 API
</br>
</br>

## 참고 문헌
**코드**
- [업비트 API 문서](https://docs.업비트.com/reference/%EC%A0%84%EC%B2%B4-%EA%B3%84%EC%A2%8C-%EC%A1%B0%ED%9A%8C)
- [py업비트 문서](https://github.com/sharebook-kr/py업비트?tab=readme-ov-file)
- [바이낸스 API 문서](https://binance-docs.github.io/apidocs/spot/en/)
- [CCXT API 문서](https://docs.ccxt.com)
-	 [바이낸스 C++ API](https://github.com/binance-exchange/binacpp)
- [텔레그램 API 사용 사례](https://charliethewanderer.medium.com/scrape-news-and-corporate-announcements-in-real-time-2-deployment-27ae489f598a)
- [파이썬에서의 벤치마킹](https://www.youtube.com/watch?v=DBoobQxqiQw)
  
**거래 개념**
- [암호 차익 거래 가이드](https://coincodecap.com/crypto-arbitrage-guide-how-to-make-money-as-a-beginner)
- [김프거래 가이드](https://charlietrip.tistory.com/19)
- [삼각 화폐 차익 거래](https://www.youtube.com/watch?v=lKu2LAgEcpU)
- [삼각 화폐 차익 거래의 작동 원리](https://www.youtube.com/clip/UgkxjqQU0dMrhLZH7qmjGzrWW1lKQGeSzllp)
- [슬리피지란?](https://www.youtube.com/watch?v=gaVYPGrxykw)
- [주문서 이해](https://www.youtube.com/watch?v=Jxyuf-cDKeg)
- [주식 가격을 결정하는 것은 누구인가?](https://www.youtube.com/watch?v=HxNH7xi4zq8)
- [깊이 차트 읽기](https://youtube.com/clip/Ugkx0c5M3OF96EjkuDo8IfXJGjiR6XCdZ8_f?si=jnnrMETCA_Mn0iLC)
- [트레이더의 마인드셋]()

**규정**
- [트래블룰](https://업비트cs.zendesk.com/hc/ko/articles/4498679629337-%ED%8A%B8%EB%9E%98%EB%B8%94%EB%A3%B0-%EC%95%8C%EC%95%84%EB%B3%B4%EA%B8%B0)
- [김프차익거래 불법인가?](https://youtube.com/shorts/YF3FK_4NOmM?si=ZgVCQ__LfEPyzb97)
