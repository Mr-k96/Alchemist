from django.shortcuts import render
from .models import EconomicNews
import os
from dotenv import load_dotenv
import requests
import pandas as pd
from collections import Counter
import re
from django.http import JsonResponse
from .models import EconomicNews
from datetime import datetime
from django.utils import timezone

# 환경 변수 로드
load_dotenv()


# views.py
def save_news(request):
    # 한국 뉴스 수집 및 저장
    kr_df = get_economic_news_kr()
    if not kr_df.empty:
        kr_saved = save_news_to_db(kr_df, "kr")

    # 미국 뉴스 수집 및 저장
    us_df = get_economic_news_us()
    if not us_df.empty:
        us_saved = save_news_to_db(us_df, "us")

    return JsonResponse(
        {
            "message": "뉴스가 성공적으로 저장되었습니다.",
            "kr_saved": kr_saved if "kr_saved" in locals() else 0,
            "us_saved": us_saved if "us_saved" in locals() else 0,
        }
    )


# 한국 경제 뉴스 데이터 수집 함수
def get_economic_news_kr():
    url = "https://serpapi.com/search"
    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google_news",
        "q": "경제 금융 시장 주식 채권 증시 환율",
        "gl": "kr",
        "hl": "ko",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()

        news_data = []
        if "news_results" in results:
            for news in results["news_results"]:
                news_data.append(
                    {
                        "title": news.get("title", ""),
                        "source": news.get("source", {}).get("name", ""),
                        "date": news.get("date", ""),
                        "snippet": news.get("snippet", ""),
                        "link": news.get("link", ""),
                    }
                )
        return pd.DataFrame(news_data)

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return pd.DataFrame()


# 미국 경제 뉴스 데이터 수집 함수
def get_economic_news_us():
    url = "https://serpapi.com/search"
    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google_news",
        "q": "Economy Financial Markets Stocks Bonds Stock Exchange Currency",
        "gl": "us",
        "hl": "en",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()

        news_data = []
        if "news_results" in results:
            for news in results["news_results"]:
                news_data.append(
                    {
                        "title": news.get("title", ""),
                        "source": news.get("source", {}).get("name", ""),
                        "date": news.get("date", ""),
                        "snippet": news.get("snippet", ""),
                        "link": news.get("link", ""),
                    }
                )
        return pd.DataFrame(news_data)

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return pd.DataFrame()


# 감성 분석 함수
def analyze_economic_sentiment(df, country="kr"):
    # 국가별 감성 키워드 정의
    keywords = {
        "kr": {
            "positive": ["상승", "증가", "호조", "개선", "성장", "회복", "강세"],
            "negative": ["하락", "감소", "악화", "위기", "리스크", "약세", "침체"],
        },
        "us": {
            "positive": [
                "growth",
                "increase",
                "gain",
                "rise",
                "surge",
                "recovery",
                "upward",
            ],
            "negative": [
                "decline",
                "decrease",
                "loss",
                "fall",
                "drop",
                "downturn",
                "recession",
            ],
        },
    }

    sentiment_scores = []
    for text in df["title"] + " " + df["snippet"]:
        pos_count = sum(
            1 for keyword in keywords[country]["positive"] if keyword in text.lower()
        )
        neg_count = sum(
            1 for keyword in keywords[country]["negative"] if keyword in text.lower()
        )
        sentiment_scores.append(pos_count - neg_count)

    return sum(sentiment_scores)


# 키워드 추출 함수
def extract_key_topics(df, country="kr"):
    text = " ".join(df["title"] + " " + df["snippet"])
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()

    stop_words = {
        "kr": ["및", "등", "를", "이", "의", "가", "은", "는"],
        "us": ["said", "says", "would", "could", "may", "might", "market", "markets"],
    }

    words = [word for word in words if word not in stop_words[country]]
    return Counter(words).most_common(5)


# 데이터베이스 저장 함수
def save_news(request):
    # 초기값 설정
    kr_saved = 0
    us_saved = 0

    try:
        # 한국 뉴스 수집 및 저장
        kr_df = get_economic_news_kr()
        if not kr_df.empty:
            kr_saved = save_news_to_db(kr_df, "kr")

        # 미국 뉴스 수집 및 저장
        us_df = get_economic_news_us()
        if not us_df.empty:
            us_saved = save_news_to_db(us_df, "us")

        return JsonResponse(
            {
                "status": "success",
                "message": "뉴스가 성공적으로 저장되었습니다.",
                "data": {
                    "kr_saved": kr_saved,
                    "us_saved": us_saved,
                    "total_saved": kr_saved + us_saved,
                },
            }
        )

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def save_news_to_db(df, country):
    """뉴스 데이터를 데이터베이스에 저장하는 함수"""
    saved_count = 0
    for _, row in df.iterrows():
        try:
            # 날짜 문자열 파싱 및 변환
            if row["date"]:
                try:
                    # "11/14/2024, 11:20 PM, +0000 UTC" 형식 처리
                    date_str = row["date"].replace(" UTC", "")
                    parsed_date = datetime.strptime(date_str, "%m/%d/%Y, %I:%M %p, %z")
                    formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # 파싱 실패 시 현재 시간으로 설정
                    formatted_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                formatted_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

            # 중복 체크
            if not EconomicNews.objects.filter(
                title=row["title"], date=formatted_date
            ).exists():
                # 새로운 뉴스 객체 생성 및 저장
                news = EconomicNews(
                    title=row["title"],
                    source=row["source"],
                    date=formatted_date,
                    snippet=row["snippet"],
                    link=row["link"],
                    sentiment_score=analyze_economic_sentiment(
                        pd.DataFrame([row]), country
                    ),
                    country=country,
                    created_at=timezone.now(),
                )
                news.save()
                saved_count += 1

        except Exception as e:
            print(f"Error saving news: {e}")
            continue

    return saved_count


# 메인 뷰 함수 - 뉴스 수집 및 분석 결과 표시
def news_analysis_view(request):
    # 한국 뉴스 수집 및 저장
    kr_df = get_economic_news_kr()
    kr_saved = 0
    kr_sentiment = 0
    kr_keywords = []

    if not kr_df.empty:
        kr_saved = save_news_to_db(kr_df, "kr")
        kr_sentiment = analyze_economic_sentiment(kr_df, "kr")
        kr_keywords = extract_key_topics(kr_df, "kr")

    # 미국 뉴스 수집 및 저장
    us_df = get_economic_news_us()
    us_saved = 0
    us_sentiment = 0
    us_keywords = []

    if not us_df.empty:
        us_saved = save_news_to_db(us_df, "us")
        us_sentiment = analyze_economic_sentiment(us_df, "us")
        us_keywords = extract_key_topics(us_df, "us")

    context = {
        "kr_news_count": len(kr_df),
        "kr_saved_count": kr_saved,
        "kr_sentiment": kr_sentiment,
        "kr_keywords": kr_keywords,
        "us_news_count": len(us_df),
        "us_saved_count": us_saved,
        "us_sentiment": us_sentiment,
        "us_keywords": us_keywords,
        "last_updated": timezone.now(),
    }

    return render(request, "news/analysis.html", context)


# 저장된 뉴스 조회 함수
def get_saved_news(request):
    # 한국어 뉴스 5개를 created_at 기준 내림차순 정렬
    kr_news = EconomicNews.objects.filter(country='kr').order_by('-date')[:5]
    # 영어 뉴스 5개를 created_at 기준 내림차순 정렬
    us_news = EconomicNews.objects.filter(country='us').order_by('-date')[:5]

    news_data = {
        'kr_news': [],
        'us_news': []
    }

    # 한국어 뉴스 데이터 가공
    for news in kr_news:
        news_data['kr_news'].append({
            'title': news.title,
            'link': news.link,
            'source': news.source,
            'date': news.date,
            'sentiment_score': news.sentiment_score,
            'created_at': news.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    # 영어 뉴스 데이터 가공
    for news in us_news:
        news_data['us_news'].append({
            'title': news.title,
            'link': news.link,
            'source': news.source,
            'date': news.date,
            'sentiment_score': news.sentiment_score,
            'created_at': news.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse({
        'status': 'success',
        'news': news_data
    })

def get_news_list(request):
    news_list = EconomicNews.objects.all().order_by('-date')[:10]  # 최신 10개 기사
    
    news_data = [{
        'title': news.title,
        'link': news.link,
        'source': news.source,
        'date': news.date
    } for news in news_list]
    
    return JsonResponse({'news': news_data})
