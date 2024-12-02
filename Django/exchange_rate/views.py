import os
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from decimal import Decimal, InvalidOperation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from .models import Exchange
from .serializers import ExchangeSerializer

# 환경 변수 로드
load_dotenv()

def get_exchange_data(url, params):
    """
    SSL 검증을 비활성화하고 재시도 전략을 적용하여 환율 데이터를 가져오는 함수
    """
    # 재시도 전략 설정
    retry_strategy = Retry(
        total=3,  # 최대 3번 재시도
        backoff_factor=1,  # 재시도 간격
        status_forcelist=[500, 502, 503, 504]  # 재시도할 HTTP 상태 코드
    )
    
    session = requests.Session()
    # SSL 검증 비활성화
    session.verify = False
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    
    try:
        # verify=False로 SSL 검증 비활성화하여 요청
        response = session.get(url, params=params, timeout=10, verify=False)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectionError as e:
        print(f"연결 오류: {e}")
        time.sleep(2)
        return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
    finally:
        session.close()

@api_view(['GET'])
def get_exchange_rate(request):
    """
    환율 정보를 API에서 가져와 데이터베이스에 저장합니다.
    """
    today = datetime.now()
    today_str = today.strftime("%Y%m%d")
    api_key = os.getenv("EXIM_API_KEY")
    if not api_key:
        return Response({"error": "API 키를 찾을 수 없습니다. 환경 변수를 확인하세요."}, status=400)
    
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': api_key,
        'searchdate': 20241122,
        'data': 'AP01'
    }

    try:
        # 수정된 get_exchange_data 함수 사용
        response = get_exchange_data(url, params)
        if response is None:
            raise requests.exceptions.RequestException("API 요청 실패")
            
        data = response.json()

        # 데이터 저장 로직은 동일하게 유지
        saved_exchanges = []
        for item in data:
            def clean_decimal(value):
                try:
                    return Decimal(value.replace(",", ""))
                except (InvalidOperation, AttributeError):
                    return None
            
            exchange, created = Exchange.objects.update_or_create(
                cur_unit=item.get('cur_unit', ''),
                defaults={
                    'cur_nm': item.get('cur_nm', ''),
                    'ttb': clean_decimal(item.get('ttb', '0')),
                    'tts': clean_decimal(item.get('tts', '0')),
                    'deal_bas_r': clean_decimal(item.get('deal_bas_r', '0')),
                    'bkpr': clean_decimal(item.get('bkpr', '0')),
                    'yy_efee_r': clean_decimal(item.get('yy_efee_r', '0')),
                    'ten_dd_efee_r': clean_decimal(item.get('ten_dd_efee_r', '0')),
                    'kftc_deal_bas_r': clean_decimal(item.get('kftc_deal_bas_r', '0')),
                    'kftc_bkpr': clean_decimal(item.get('kftc_bkpr', '0')),
                }
            )
            saved_exchanges.append(exchange)

        serializer = ExchangeSerializer(saved_exchanges, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except requests.exceptions.RequestException:
        # API 호출 실패 시 DB 데이터 반환
        saved_data = Exchange.objects.all()
        if saved_data.exists():
            serializer = ExchangeSerializer(saved_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'error': '외부 API 호출과 로컬 데이터 조회 모두 실패했습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response({"error": f"예상치 못한 오류: {str(e)}"}, status=500)