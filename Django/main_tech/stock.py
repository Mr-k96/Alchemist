import os
from dotenv import load_dotenv
load_dotenv()

import requests
import json

# 토큰 발급 함수
def get_access_token():
    url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
    
    headers = {
        "content-type": "application/json"
    }
    
    body = {
        "grant_type": "client_credentials",
        "appkey": os.getenv("APP_KEY"),
        "appsecret": os.getenv("APP_SECRET")
    }
    
    res = requests.post(url, headers=headers, data=json.dumps(body))
    return res.json()["access_token"]

# ETF 현재가 조회 함수 
def get_etf_price(access_token, etf_code):
    url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-price"
    
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appKey": os.getenv("APP_KEY"),
        "appSecret": os.getenv("APP_SECRET"),
        "tr_id": "FHKST01010100"
    }
    
    params = {
        "fid_cond_mrkt_div_code": "J", # 주식, ETF, ETN
        "fid_input_iscd": etf_code     # ETF 종목코드
    }
    
    res = requests.get(url, headers=headers, params=params)
    return res.json()

# ETF 일별 시세 조회 함수
def get_etf_daily_price(access_token, etf_code):
    url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-daily-price"
    
    headers = {
        "Content-Type": "application/json", 
        "authorization": f"Bearer {access_token}",
        "appKey": os.getenv("APP_KEY"),
        "appSecret": os.getenv("APP_SECRET"),
        "tr_id": "FHKST01010400"
    }
    
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": etf_code,
        "fid_period_div_code": "D",  # D:일별, W:주별, M:월별
        "fid_org_adj_prc": "1"       # 0:수정주가, 1:원주가
    }
    
    res = requests.get(url, headers=headers, params=params)
    return res.json()

# 실행 예시
if __name__ == "__main__":
    # ETF 종목코드 예시 (WON 한국부동산TOP3플러스: 480460)
    ETF_CODE = "448290"
    
    # 1. 토큰 발급
    access_token = get_access_token()
    
    # 2. 현재가 조회
    current_price = get_etf_price(access_token, ETF_CODE)
    print("현재가 정보:", current_price['output']['stck_prpr'])
    
    # 3. 일별 시세 조회
    daily_prices = get_etf_daily_price(access_token, ETF_CODE)
    for price in daily_prices['output']:
        print(f"일자: {price['stck_bsop_date']}, 종가: {price['stck_clpr']}")