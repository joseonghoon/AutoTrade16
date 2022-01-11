import time
import pyupbit
import datetime
import requests

access = "bsYWp701yJmtgcHxwvVxgAdrlxJYyE8UU1uvMpQa"
secret = "jZBIU6tTAkrr6aXPZRUSwdPkEGSLiBqdKaPxxORm"

def send_message(msg):
    """slcak 메세지 보내기"""
    url = "https://hooks.slack.com/services/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"
    data = {'text':msg}
    resp = requests.post(url=url, json=data)
    return resp

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
send_message("login and start")

# print(get_target_price('KRW-XRP', 0.5))
# print(get_current_price('KRW-XRP'))

# print(get_target_price('KRW-BTC', 0.5))
# print(get_current_price('KRW-BTC'))

# print(get_target_price('KRW-ETH', 0.5))
# print(get_current_price('KRW-ETH'))

# print(get_target_price('KRW-BORA', 0.5))
# print(get_current_price('KRW-BORA'))


 # 자동매매 시작
while True:
     try:
         now = datetime.datetime.now()
         start_time = get_start_time("KRW-XRP")
         end_time = start_time + datetime.timedelta(days=1)

         if start_time < now < end_time - datetime.timedelta(seconds=10):
             #리플
             target_price = get_target_price("KRW-XRP", 0.5)
             current_price = get_current_price("KRW-XRP")
             if target_price < current_price:
                 krw = get_balance("KRW")
                 if krw > 5000:
                     buy_xrp = upbit.buy_market_order("KRW-XRP", krw*0.9995)
                     send_message("XRP buy : " +str(buy_xrp))
             #비트코인        
             target_price = get_target_price("KRW-BTC", 0.5)
             current_price = get_current_price("KRW-BTC")
             if target_price < current_price:
                 krw = get_balance("KRW")
                 if krw > 5000:
                     buy_btc = upbit.buy_market_order("KRW-BTC", krw*0.9995)
                     send_message("BTC buy : " +str(buy_btc))
             #이더리움
             target_price = get_target_price("KRW-ETH", 0.5)
             current_price = get_current_price("KRW-ETH")
             if target_price < current_price:
                 krw = get_balance("KRW")
                 if krw > 5000:
                     buy_eth = upbit.buy_market_order("KRW-ETH", krw*0.9995)
                     send_message("ETH buy : " +str(buy_eth))
             #보라        
             target_price = get_target_price("KRW-BORA", 0.5)
             current_price = get_current_price("KRW-BORA")
             if target_price < current_price:
                 krw = get_balance("KRW")
                 if krw > 5000:
                     buy_bora = upbit.buy_market_order("KRW-BORA", krw*0.9995) 
                     send_message("BORA buy : " +str(buy_bora))        
                     
         else:
             #리플
             xrp = get_balance("XRP")
             if xrp > 0.00008:
                 sell_xrp = upbit.sell_market_order("KRW-XRP", xrp*0.9995)
                 send_message("XRP sell : " +str(sell_xrp)) 
            #비트코인
             btc = get_balance("BTC")
             if btc > 0.00008:
                 sell_btc = upbit.sell_market_order("KRW-BTC", btc*0.9995)
                 send_message("BTC sell : " +str(sell_btc)) 
             #이더리움
             eth = get_balance("ETH")
             if eth > 0.00008:
                 upbit.sell_market_order("KRW-ETH", eth*0.9995)
                 send_message("ETH sell : " +str(sell_xrp)) 
            #보라
             bora = get_balance("BORA")
             if bora > 0.00008:
                 sell_bora = upbit.sell_market_order("KRW-BORA", bora*0.9995)
                 send_message("BORa sell : " +str(sell_bora))           
         time.sleep(1)
     except Exception as e:
         print(e)
         send_message("ERROR")
         time.sleep(1)
