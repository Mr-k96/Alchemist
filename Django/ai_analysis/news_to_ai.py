import os
import sys
from datetime import datetime, timedelta
from django.utils import timezone

# 프로젝트 루트 디렉토리의 상위 경로를 시스템 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Django 설정
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Archemist.settings')  # 여기를 수정
django.setup()

from news.models import EconomicNews

def get_news_by_country(country_code, days=30):
    """
    특정 국가의 최근 뉴스 데이터를 조회하는 함수
    
    Args:
        country_code (str): 국가 코드 ('kr' 또는 'us')
        days (int): 조회할 기간 (일 단위, 기본값 30일)
    
    Returns:
        list: 뉴스 데이터 리스트
    """
    one_month_ago = timezone.now() - timedelta(days=days)
    
    news = EconomicNews.objects.filter(
        country=country_code.lower(),
        date__gte=one_month_ago
    ).order_by('-date')
    
    news_dict = news.values('title', 'date', 'sentiment_score')
    return list(news_dict)

# 함수 사용 예시
if __name__ == "__main__":
    # 한국 뉴스 조회
    kr_news_list = get_news_by_country('kr')
    print("한국 뉴스:", kr_news_list)
    
    # 미국 뉴스 조회
    us_news_list = get_news_by_country('us')
    print("미국 뉴스:", us_news_list)