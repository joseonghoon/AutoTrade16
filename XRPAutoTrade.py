import time
import pyupbit
import datetime
import requests

access = "bsYWp701yJmtgcHxwvVxgAdrlxJYyE8UU1uvMpQa"
secret = "jZBIU6tTAkrr6aXPZRUSwdPkEGSLiBqdKaPxxORm"
myToken = ""


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
         xrp_target_price = get_target_price("KRW-XRP", 0.3)
         ada_target_price = get_target_price("KRW-ADA", 0.6)
         etc_target_price = get_target_price("KRW-ETC", 0.5)
         bora_target_price = get_target_price("KRW-BORA", 0.2)
         doge_target_price = get_target_price("KRW-DOGE", 0.2)
         
         #잔고 조회    
         krw = get_balance("KRW")
         xrp = upbit.get_balance("KRW-XRP")
         ada = upbit.get_balance("KRW-ADA")
         etc = upbit.get_balance("KRW-ETC")
         bora = upbit.get_balance("KRW-BORA")
         doge = upbit.get_balance("KRW-DOGE") 
         
         if now == end_time + datetime.timedelta(seconds=30):
             #장 시작시 매수 목표가 알림
             post_message(myToken,"#trade","today target price" 
                        + "\nXRP : "+ str(xrp_target_price) 
                        + "\nADA : "+ str(ada_target_price)
                        + "\nETC : "+ str(etc_target_price) 
                        + "\nBORA : "+ str(bora_target_price)
                        + "\nDOGE : "+ str(doge_target_price))   

         elif start_time < now < end_time - datetime.timedelta(seconds=10):
             # 9900원 이상 보유시 1만원 매수 (2칸차이 매수)
             #리플
             current_price = get_current_price("KRW-XRP")
             if xrp_target_price <= current_price <= xrp_target_price + (xrp_target_price*0.002):
                 if krw > 9900 and xrp < 2:
                     upbit.buy_market_order("KRW-XRP", 9999)
                     post_message(myToken,"#trade", "XRP buy")
             #에이다
             current_price = get_current_price("KRW-ADA")
             if ada_target_price < current_price <= ada_target_price + (ada_target_price*0.006):
                 if krw > 9900 and ada < 2:
                     upbit.buy_market_order("KRW-ADA", 9999)
                     post_message(myToken,"#trade", "ADA buy")
             #이더리움클래식
             current_price = get_current_price("KRW-ETC")
             if etc_target_price < current_price <= etc_target_price + (etc_target_price*0.002):
                 if krw > 9900 and etc < 0.2:
                     upbit.buy_market_order("KRW-ETC", 9999)
                     post_message(myToken,"#trade", "ETC buy")
             #보라        
             current_price = get_current_price("KRW-BORA")
             if bora_target_price < current_price <= bora_target_price + (bora_target_price*0.008):
                 if krw > 9900 and bora < 2:
                     upbit.buy_market_order("KRW-BORA", 9999) 
                     post_message(myToken,"#trade", "BORA buy") 
             #도지       
             current_price = get_current_price("KRW-DOGE")
             if doge_target_price < current_price <= doge_target_price + (doge_target_price*0.01):
                 if krw > 9900 and doge < 2:
                     upbit.buy_market_order("KRW-DOGE", 9999) 
                     post_message(myToken,"#trade", "DOGE buy")  
                     
             #매도 (4칸차이나면 매도)
             #리플
             current_price = get_current_price("KRW-XRP")
             if xrp > 0.0000:
                if current_price >= xrp_target_price+(xrp_target_price*0.01):
                    upbit.sell_market_order("KRW-XRP", xrp)
                    post_message(myToken,"#trade", "XRP sell")
             #에이다
             if ada > 0.0000:
                current_price = get_current_price("KRW-ADA")
                if current_price >= ada_target_price+(ada_target_price*0.01):
                    upbit.sell_market_order("KRW-ADA", ada)
                    post_message(myToken,"#trade", "ADA sell")
             #이더리움클래식
             if etc > 0.0000:
                current_price = get_current_price("KRW-ETC")
                if current_price >= etc_target_price+(etc_target_price*0.008):
                    upbit.sell_market_order("KRW-ETC", etc)
                    post_message(myToken,"#trade", "ETC sell")
             #보라
             if bora > 0.0000:
                current_price = get_current_price("KRW-BORA")
                if current_price >= bora_target_price+(bora_target_price*0.035):
                    upbit.sell_market_order("KRW-BORA", bora)
                    post_message(myToken,"#trade", "BORA sell")
             #도지
             if doge > 0.0000:
                current_price = get_current_price("KRW-DOGE")
                if current_price >= doge_target_price+(doge_target_price*0.1):
                    upbit.sell_market_order("KRW-DOGE", doge)
                    post_message(myToken,"#trade", "DOGE sell")
                           
                     
         else:
             #리플
             if xrp > 0.00008:
                 upbit.sell_market_order("KRW-XRP", xrp)
                 post_message(myToken,"#trade", "XRP sell")
             #에이다
             if ada > 0.00008:
                 upbit.sell_market_order("KRW-ADA", ada)
                 post_message(myToken,"#trade", "ADA sell")
             #이더리움클래식
             if etc > 0.00008:
                 upbit.sell_market_order("KRW-ETC", etc)
                 post_message(myToken,"#trade", "ETC sell") 
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
