import os
from dotenv import load_dotenv
load_dotenv()
import requests
import pprint

# 예금 데이터
def get_deposit_products():
    api_key = os.getenv("FSS_API_KEY")
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': api_key,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(url, params=params).json()
    result_data = response['result']
    
    base_list = result_data['baseList']
    option_list = result_data['optionList']
    
    result = []
    
    for base in base_list:
        options = [opt for opt in option_list if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
        product_info = {
            '금융상품코드': base['fin_prdt_cd'],
            '금융회사명': base['kor_co_nm'],
            '상품명': base['fin_prdt_nm'],
            '금리정보': [{
                '저축기간': opt['save_trm'],
                '기본금리': format(float(opt['intr_rate'] or 0), '.2f'),
                '최고우대금리': format(float(opt['intr_rate2'] or 0), '.2f')
            } for opt in options]
        }
        result.append(product_info)
    
    return result

# 아래 코드는 수정하지 않습니다.
if __name__ == '__main__':
    # json 형태의 데이터 반환
    result = get_deposit_products()
    # prrint.prrint(): json 을 보기 좋은 형식으로 출력
    pprint.pprint(result)