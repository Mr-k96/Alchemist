import os
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
import pprint
from .models import DepositProduct, DepositOption
from .serializers import DepositProductSerializer

load_dotenv()

def get_deposit_products():
    api_key = os.getenv("FSS_API_KEY")
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': api_key,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 오류 검사
        response_data = response.json()
        
        # result 키가 있는지 확인
        if 'result' not in response_data:
            return []
            
        result_data = response_data['result']
        
        # baseList와 optionList가 있는지 확인
        base_list = result_data.get('baseList', [])
        option_list = result_data.get('optionList', [])
        
        if not base_list or not option_list:
            print("데이터가 비어있습니다.")
            return []
        
        result = []
        for base in base_list:
            options = [opt for opt in option_list if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
            product_info = {
                '금융상품코드': base.get('fin_prdt_cd', ''),
                '금융회사명': base.get('kor_co_nm', ''),
                '상품명': base.get('fin_prdt_nm', ''),
                '상품정보': [{
                    '금융상품설명': base.get('etc_note', ''),
                    '가입대상': base.get('join_member', ''),
                    '가입방법': base.get('join_way', ''),
                    '우대조건': base.get('spcl_cnd', ''),
                    '가입제한': base.get('join_deny', ''),
                }],
                '금리정보': [{
                    '저축기간': opt.get('save_trm', ''),
                    '기본금리': format(float(opt.get('intr_rate', 0) or 0), '.2f'),
                    '최고우대금리': format(float(opt.get('intr_rate2', 0) or 0), '.2f')
                } for opt in options]
            }
            result.append(product_info)
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return []
    except ValueError as e:
        print(f"JSON 파싱 중 오류 발생: {e}")
        return []
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        return []

@api_view(['GET'])
def save_deposit_products(request):
    products_data = get_deposit_products()
    
    saved_products = []
    for product in products_data:
        # 상품 정보 저장
        deposit_product = DepositProduct.objects.get_or_create(
            fin_prdt_cd=product['금융상품코드'],
            defaults={
                'kor_co_nm': product['금융회사명'],
                'fin_prdt_nm': product['상품명'],
            }
        )[0]
        
        # 기존 옵션 삭제 후 새로운 옵션 저장
        DepositOption.objects.filter(product=deposit_product).delete()
        
        # 옵션 정보 저장
        for option in product['금리정보']:
            DepositOption.objects.create(
                product=deposit_product,
                save_trm=int(option['저축기간']),
                intr_rate=float(option['기본금리']),
                intr_rate2=float(option['최고우대금리']),
            )
        
        saved_products.append(deposit_product)
    
    serializer = DepositProductSerializer(saved_products, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# CLI 실행을 위한 코드
if __name__ == '__main__':
    result = get_deposit_products()
    pprint.pprint(result)
    
@api_view(['GET'])
def get_all_deposit_products(request):
    """모든 예금 상품 조회 (필터링 및 정렬 기능 추가)"""
    products = DepositProduct.objects.all()
    
    # 금융회사명으로 필터링
    company = request.query_params.get('company', None)
    if company:
        products = products.filter(kor_co_nm__icontains=company)
    
    # 상품명으로 필터링
    product_name = request.query_params.get('product_name', None)
    if product_name:
        products = products.filter(fin_prdt_nm__icontains=product_name)
    
    # 정렬
    ordering = request.query_params.get('ordering', '-created_at')
    if ordering:
        products = products.order_by(ordering)
    
    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_deposit_product_detail(request, fin_prdt_cd):
    """특정 예금 상품 상세 조회"""
    try:
        product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
        serializer = DepositProductSerializer(product)
        return Response(serializer.data)
    except DepositProduct.DoesNotExist:
        return Response({'error': '상품을 찾을 수 없습니다.'}, 
                       status=status.HTTP_404_NOT_FOUND)