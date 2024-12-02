import os
from dotenv import load_dotenv
load_dotenv()

import requests
from datetime import datetime
import pandas as pd
from collections import Counter
import re

# 4-1. 한국 경제 뉴스데이터 가져오기
def get_economic_news_kr():
    # API 엔드포인트 및 파라미터 설정
    url = "https://serpapi.com/search"
    
    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google_news",
        "q": "경제 금융 시장 주식 채권 증시 환율",
        "gl": "kr",
        "hl": "ko"
    }

    try:
        # GET 요청 보내기
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 에러 체크
        
        results = response.json()
        
        # 뉴스 데이터 추출
        news_data = []
        if 'news_results' in results:
            for news in results['news_results']:
                news_data.append({
                    'title': news.get('title', ''),
                    'source': news.get('source', {}).get('name', ''),
                    'date': news.get('date', ''),
                    'snippet': news.get('snippet', ''),
                    'link': news.get('link', '')
                })
        
        return pd.DataFrame(news_data)
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return pd.DataFrame()

def analyze_economic_sentiment(df):
    # 감성 분석을 위한 키워드 정의
    positive_keywords = ['상승', '증가', '호조', '개선', '성장', '회복', '강세']
    negative_keywords = ['하락', '감소', '악화', '위기', '리스크', '약세', '침체']
    
    sentiment_scores = []
    for text in df['title'] + ' ' + df['snippet']:
        pos_count = sum(1 for keyword in positive_keywords if keyword in text)
        neg_count = sum(1 for keyword in negative_keywords if keyword in text)
        sentiment_scores.append(pos_count - neg_count)
    
    return sum(sentiment_scores)

def extract_key_topics(df):
    # 텍스트 결합
    text = ' '.join(df['title'] + ' ' + df['snippet'])
    # 특수문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    
    # 불용어 처리
    stop_words = ['및', '등', '를', '이', '의', '가', '은', '는']
    words = [word for word in words if word not in stop_words]
    
    return Counter(words).most_common(5)

def main():
    print(f"경제 뉴스 분석 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 뉴스 데이터 수집
    df = get_economic_news_kr()
    if df.empty:
        print("뉴스 데이터를 가져오는데 실패했습니다.")
        return
        
    print(f"\n수집된 뉴스 기사 수: {len(df)}")
    
    # 감성 분석
    sentiment_score = analyze_economic_sentiment(df)
    print("\n시장 분위기 분석:")
    if sentiment_score > 0:
        print(f"현재 시장 분위기: 긍정적 (점수: {sentiment_score})")
    elif sentiment_score < 0:
        print(f"현재 시장 분위기: 부정적 (점수: {sentiment_score})")
    else:
        print("현재 시장 분위기: 중립적")
    
    # 주요 키워드 분석
    print("\n주요 키워드:")
    for word, count in extract_key_topics(df):
        print(f"- {word}: {count}회 언급")
    
    # 최신 헤드라인
    print("\n최신 주요 헤드라인:")
    for _, row in df.head(5).iterrows():
        print(f"- {row['title']} ({row['source']}) ({row['link']})")

if __name__ == "__main__":
    main()
    
# 4-2. 미국 경제 뉴스데이터 가져오기    
def get_us_economic_news_us():
    # API 엔드포인트 및 파라미터 설정
    url = "https://serpapi.com/search"
    
    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google_news",
        "q": "Economy Financial Markets Stocks Bonds Stock ExchangeCurrency",
        "gl": "us",
        "hl": "en"
    }

    try:
        # GET 요청 보내기
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 에러 체크
        
        results = response.json()
        
        # 뉴스 데이터 추출
        news_data = []
        if 'news_results' in results:
            for news in results['news_results']:
                news_data.append({
                    'title': news.get('title', ''),
                    'source': news.get('source', {}).get('name', ''),
                    'date': news.get('date', ''),
                    'snippet': news.get('snippet', ''),
                    'link': news.get('link', '')
                })
        
        return pd.DataFrame(news_data)
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return pd.DataFrame()

def analyze_economic_sentiment(df):
    # 감성 분석을 위한 키워드 정의
    positive_keywords = ['growth', 'increase', 'gain', 'rise', 'surge', 'recovery', 'upward']
    negative_keywords = ['decline', 'decrease', 'loss', 'fall', 'drop', 'downturn', 'recession']
    
    sentiment_scores = []
    for text in df['title'] + ' ' + df['snippet']:
        pos_count = sum(1 for keyword in positive_keywords if keyword in text)
        neg_count = sum(1 for keyword in negative_keywords if keyword in text)
        sentiment_scores.append(pos_count - neg_count)
    
    return sum(sentiment_scores)

def extract_key_topics(df):
    # 텍스트 결합
    text = ' '.join(df['title'] + ' ' + df['snippet'])
    # 특수문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    
    # 불용어 처리
    stop_words = ['said', 'says', 'would', 'could', 'may', 'might', 'market', 'markets']
    words = [word for word in words if word not in stop_words]
    
    return Counter(words).most_common(5)

def main():
    print(f"경제 뉴스 분석 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 뉴스 데이터 수집
    df = get_us_economic_news_us()
    
    if df.empty:
        print("뉴스 데이터를 가져오는데 실패했습니다.")
        return
        
    print(f"\n수집된 뉴스 기사 수: {len(df)}")
    
    # 감성 분석
    sentiment_score = analyze_economic_sentiment(df)
    print("\n시장 분위기 분석:")
    if sentiment_score > 0:
        print(f"현재 시장 분위기: 긍정적 (점수: {sentiment_score})")
    elif sentiment_score < 0:
        print(f"현재 시장 분위기: 부정적 (점수: {sentiment_score})")
    else:
        print("현재 시장 분위기: 중립적")
    
    # 주요 키워드 분석
    print("\n주요 키워드:")
    for word, count in extract_key_topics(df):
        print(f"- {word}: {count}회 언급")
    
    # 최신 헤드라인
    print("\n최신 주요 헤드라인:")
    for _, row in df.head(5).iterrows():
        print(f"- {row['title']} ({row['source']})")

if __name__ == "__main__":
    main()