"""
한국투자증권 오픈 API를 활용한 ETF 시세 조회 및 포트폴리오 분석 모듈
- 토큰 관리 및 ETF 현재가/주별시세 조회 기능 제공
- 토큰은 24시간 유효하며 만료 시 자동 갱신
- 120개의 주봉 데이터를 수집하여 포트폴리오 분석 수행
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta
from .analysis import analyze_portfolio

# .env 파일에서 환경변수 로드 
load_dotenv()

class TokenManager:
    """토큰 관리 클래스
    - access_token: 발급받은 토큰
    - token_expires_at: 토큰 만료 시각
    - 토큰의 재사용성을 높이고 불필요한 발급을 방지
    """
    def __init__(self):
        self.access_token = None
        self.token_expires_at = None
    
    def get_token(self):
        """토큰 조회/발급 메서드
        - 유효한 토큰이 있으면 재사용
        - 만료되었거나 없으면 새로 발급
        Returns:
            str: 유효한 access token
        """
        current_time = datetime.now()
        
        if not self.access_token or not self.token_expires_at or current_time >= self.token_expires_at:
            self.access_token = get_access_token()
            # 토큰 유효기간을 23시간으로 설정하여 만료 직전 갱신 방지
            self.token_expires_at = current_time + timedelta(hours=23)
            
        return self.access_token

# TokenManager 인스턴스 생성 - 앱 전체에서 토큰 공유
token_manager = TokenManager()

def get_access_token():
    """한국투자증권 API 토큰 발급 함수
    Returns:
        str: 발급받은 access token
    """
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

def get_etf_weekly_price(access_token, etf_code, page=1):
    """ETF 주별 시세 조회 함수"""
    try:
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
            "fid_period_div_code": "W",
            "fid_org_adj_prc": "1",
            "tr_cont": "N" if page == 1 else "Y"
        }
        
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()  # HTTP 오류 확인
        return res.json()
        
    except requests.exceptions.RequestException as e:
        print(f"API request error: {str(e)}")
        return {'error': str(e)}
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return {'error': 'Invalid JSON response'}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {'error': str(e)}

@api_view(['POST'])
def get_stock_data(request):
    try:
        etf_codes = request.data.get('codes')
        print(f"\n=== ETF 데이터 수집 시작 ===") # 디버깅용
        print(f"요청된 ETF 코드: {etf_codes}") 
        print(f"요청된 ETF 코드 수: {len(etf_codes)}")

        if not etf_codes:
            return Response({
                'status': 'error',
                'message': '종목 코드가 제공되지 않았습니다.'
            }, status=400)
        
        access_token = token_manager.get_token()
        result = {}
        
        for etf_code in etf_codes:
            try:
                formatted_code = str(etf_code).zfill(6)
                print(f"처리 중인 ETF: {formatted_code}")  # 디버깅용
                
                daily_prices = []
                
                # 5년 데이터 수집 시도
                try:
                    for page in range(1, 9):
                        daily_price_data = get_etf_weekly_price(access_token, formatted_code, page)
                        if not daily_price_data:
                            print(f"데이터 없음: {formatted_code}, page {page}")
                            continue
                            
                        if 'output' not in daily_price_data:
                            print(f"잘못된 응답: {formatted_code}, page {page}")
                            continue

                        current_data = daily_price_data['output']    
                        daily_prices.extend(daily_price_data['output'])
                        print(f"- Page {page}: {len(current_data)}개 데이터 수집 (누적: {len(daily_prices)}개)")
                        
                except Exception as e:
                    print(f"데이터 수집 오류: {str(e)}")
                    continue
                
                if daily_prices:
                    result[etf_code] = {
                        'daily_prices': {'output': daily_prices}
                    }
                else:
                    print(f"수집된 데이터 없음: {formatted_code}")
                    result[etf_code] = {'error': '데이터를 찾을 수 없습니다.'}
                
            except Exception as e:
                print(f"ETF {etf_code} 처리 중 오류: {str(e)}")
                result[etf_code] = {'error': str(e)}
        
        # 분석 수행 전 데이터 검증
        if not any('daily_prices' in data for data in result.values()):
            return Response({
                'status': 'error',
                'message': '분석 가능한 데이터가 없습니다.'
            }, status=404)
            
        try:
            analysis_result = analyze_portfolio(result)
            return Response({
                'status': 'success',
                'data': result,
                'analysis': analysis_result
            })
        except Exception as e:
            print(f"분석 오류: {str(e)}")
            return Response({
                'status': 'error',
                'data': result,
                'message': f'분석 중 오류 발생: {str(e)}'
            })
            
    except Exception as e:
        print(f"서버 오류: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)