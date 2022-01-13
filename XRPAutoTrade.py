import time
import pyupbit
import datetime
import requests

access = "bsYWp701yJmtgcHxwvVxgAdrlxJYyE8UU1uvMpQa"
secret = "jZBIU6tTAkrr6aXPZRUSwdPkEGSLiBqdKaPxxORm"
myToken = "xoxb-2925112561509-2951781580992-5CcEVWHfgGF6qDxkCKxPkYk1"


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]



 # 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
post_message(myToken,"#trade", "login success and start")


 # 자동매매 시작
while True:
     try:
         #시간 설정
         now = datetime.datetime.now()
         start_time = get_start_time("KRW-XRP")
         end_time = start_time + datetime.timedelta(days=1)
         
         #매수 목표가 설정
         xrp_target_price = get_target_price("KRW-XRP", 0.4)
         btc_target_price = get_target_price("KRW-BTC", 0.6)
         eth_target_price = get_target_price("KRW-ETH", 0.4)
         bora_target_price = get_target_price("KRW-BORA", 0.3)
         doge_target_price = get_target_price("KRW-DOGE", 0.5)
         
         #잔고 조회    
         krw = get_balance("KRW")
         xrp = get_balance("KRW-XRP")
         btc = get_balance("KRW-BTC")
         eth = get_balance("KRW-ETH")
         bora = get_balance("KRW-BORA")
         doge = get_balance("KRW-DOGE") 
         
         if now == start_time:
             #장 시작시 매수 목표가 알림
             post_message(myToken,"#trade","today target price" 
                        + "\nXRP : "+ str(xrp_target_price) 
                        + "\nBTC : "+ str(btc_target_price)
                        + "\nETH : "+ str(eth_target_price) 
                        + "\nBORA : "+ str(bora_target_price)
                        + "\nDOGE : "+ str(doge_target_price))   

         if start_time < now < end_time - datetime.timedelta(seconds=10):
             # 9900원 이상 보유시 1만원 매수
             #리플
             current_price = get_current_price("KRW-XRP")
             if xrp_target_price < current_price:
                 if krw > 9900 & xrp < 2:
                     upbit.buy_market_order("KRW-XRP", 9999)
                     post_message(myToken,"#trade", "XRP buy")
             #비트코인        
             current_price = get_current_price("KRW-BTC")
             if btc_target_price < current_price:
                 if krw > 9900 & btc < 0.0002:
                     upbit.buy_market_order("KRW-BTC", 9999)
                     post_message(myToken,"#trade", "BTC buy")
             #이더리움
             current_price = get_current_price("KRW-ETH")
             if eth_target_price < current_price:
                 if krw > 9900 & eth < 0.002:
                     upbit.buy_market_order("KRW-ETH", 9999)
                     post_message(myToken,"#trade", "ETH buy")
             #보라        
             current_price = get_current_price("KRW-BORA")
             if bora_target_price < current_price:
                 if krw > 9900 & bora < 2:
                     upbit.buy_market_order("KRW-BORA", 9999) 
                     post_message(myToken,"#trade", "BORA buy") 
            #도지       
             current_price = get_current_price("KRW-DOGE")
             if doge_target_price < current_price:
                 if krw > 9900 & doge < 2:
                     upbit.buy_market_order("KRW-DOGE", 9999) 
                     post_message(myToken,"#trade", "DOGE buy")       
                     
         else:
             #리플
             if xrp > 0.00008:
                 upbit.sell_market_order("KRW-XRP", xrp)
                 post_message(myToken,"#trade", "XRP sell")
            #비트코인
             if btc > 0.00008:
                 upbit.sell_market_order("KRW-BTC", btc)
                 post_message(myToken,"#trade", "BTC sell")
             #이더리움
             if eth > 0.00008:
                 upbit.sell_market_order("KRW-ETH", eth)
                 post_message(myToken,"#trade", "ETH sell") 
            #보라
             if bora > 0.00008:
                 upbit.sell_market_order("KRW-BORA", bora)
                 post_message(myToken,"#trade", "BORA sell")
            #도지
             if bora > 0.00008:
                 upbit.sell_market_order("KRW-DOGE", doge)
                 post_message(myToken,"#trade", "DOGE sell")           
         time.sleep(1)
     except Exception as e:
         print(e)
         post_message(myToken,"#trade", "ERROR")
         time.sleep(1)
