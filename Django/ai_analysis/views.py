from django.http import JsonResponse
from openai import RateLimitError, APIError, OpenAI
from dotenv import load_dotenv
import json
from .news_to_ai import get_news_by_country
from datetime import datetime, timedelta
import investpy, os
from django.views.decorators.csrf import csrf_exempt
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def get_economic_calendar():
    """경제 캘린더 데이터를 조회하는 함수"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 최근 6달 데이터만 조회

    from_date = start_date.strftime("%d/%m/%Y")
    to_date = end_date.strftime("%d/%m/%Y")

    try:
        calendar = investpy.economic_calendar(
            from_date=from_date,
            to_date=to_date,
            countries=["united states", "south korea", "china"],
            importances=["high"],
            time_zone=None,
            time_filter="time_only",
        )

        # NaN 값이 있는 행 제거 및 날짜 기준 내림차순 정렬
        calendar = calendar[calendar["importance"].notna()]
        calendar = calendar.sort_values("date", ascending=False)

        calendar["date"] = pd.to_datetime(calendar["date"], dayfirst=True)
        calendar["date"] = calendar["date"].dt.strftime("%Y-%m-%d")  # 문자열로 포맷팅

        selected_columns = [
            "date",
            "time",
            "zone",
            "event",
            "importance",
            "actual",
            "forecast",
            "previous",
        ]
        return calendar[selected_columns].to_dict("records")
    except Exception as e:
        logger.error(f"경제 캘린더 데이터 조회 오류: {e}")
        return []


def calculate_mean(data):
    if len(data) == 0:
        return np.nan
    return np.mean(data)


def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


@csrf_exempt
def ai_analysis(request):
    """AI 분석을 수행하는 API 엔드포인트"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OpenAI API 키가 설정되지 않았습니다.")
            return JsonResponse({"error": "API 키가 설정되지 않았습니다."}, status=500)
        # 요청 데이터 파싱
        portfolio_data = json.loads(request.body)
        kr_news_list = get_news_by_country("kr")
        us_news_list = get_news_by_country("us")
        calendar_data = get_economic_calendar()

        # 분석용 데이터 구조화
        analysis_data = {
            "portfolio_data": portfolio_data,
            "kr_news": kr_news_list,
            "us_news": us_news_list,
            "economic_calendar": calendar_data,
        }

        load_dotenv()
        # OpenAI API 설정
        client = OpenAI()

        # AI 분석 요청
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """금융투자전문가로서 다음의 분석 기준과 평가 지표를 바탕으로 포트폴리오를 분석하고 전문적인 자문을 제공합니다. 제공된 포트폴리오에 대해 최신 경제지표와 뉴스 데이터를 기반으로 평가하고, 투자 초보자도 이해할 수 있도록 상세한 설명을 제공합니다. 응답은 한국어를 사용하며 JSON 방식으로 합니다.

            {
                "market_analysis": {
                    "current_trends": {
                        "economic_indicators": "금리, 물가지수(CPI/PPI), 고용지표 분석",
                        "sector_analysis": "업종별 성과 및 전망",
                        "market_sentiment": "투자심리 지표 분석"
                    },
                    "global_impact": {
                        "macro_factors": "글로벌 경제 현황 분석",
                        "geopolitical_risks": "지정학적 리스크 평가",
                        "currency_effects": "환율 영향 분석"
                    }
                },
                "portfolio_analysis": {
                    "performance": {
                        "absolute_returns": "절대수익률 분석",
                        "relative_returns": "상대수익률 분석",
                        "risk_adjusted_returns": "위험조정수익률 분석"
                    },
                    "risk_metrics": {
                        "variance": "변동성 지표",
                        "correlation": "자산간 상관관계",
                        "beta": "시장민감도",
                        "var": "Value at Risk",
                        "stress_test": "스트레스 테스트 결과"
                    },
                    "recommendation": {
                        "asset_allocation": "자산배분 제안",
                        "rebalancing": "리밸런싱 전략",
                        "risk_management": "위험관리 방안"
                    }
                },
                "risk_analysis": {
                    "market_risks": {
                        "systematic_risk": "시스템적 리스크 요인",
                        "interest_rate_risk": "금리 리스크",
                        "liquidity_risk": "유동성 리스크"
                    },
                    "portfolio_risks": {
                        "concentration_risk": "집중 위험",
                        "currency_risk": "환위험",
                        "credit_risk": "신용위험"
                    }
                }
            }
            
            분석 시 다음 사항을 반드시 포함하여 평가해주세요:
            1. 최신 경제지표와 시장 동향 반영
            2. 글로벌 매크로 환경이 포트폴리오에 미치는 영향
            3. 위험조정수익률 기반의 성과 평가
            4. 리스크 요인별 정량적/정성적 분석
            5. 구체적인 투자전략 및 리밸런싱 제안""",
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        analysis_data, ensure_ascii=False, default=str
                    ),
                },
            ],
            response_format={"type": "json_object"},
        )

        # 응답 데이터 표준화
        standardized_result = standardize_response(response)
        return JsonResponse(standardized_result)

    except RateLimitError as e:
        logger.error(f"OpenAI Rate Limit 에러 발생: {str(e)}")
        return JsonResponse(
            {
                "error": "서비스가 일시적으로 사용량을 초과했습니다. 잠시 후 다시 시도해주세요.",
                "detail": str(e),
            },
            status=429,
        )
    except APIError as e:
        logger.error(f"OpenAI API 에러 발생: {str(e)}")
        return JsonResponse(
            {"error": "API 서비스 오류가 발생했습니다.", "detail": str(e)}, status=500
        )
    except Exception as e:
        logger.error(f"AI 분석 처리 중 오류 발생: {str(e)}")
        return JsonResponse(
            {"error": "서비스 처리 중 오류가 발생했습니다."}, status=500
        )


def standardize_response(raw_response):
    """AI 응답을 표준화된 형식으로 변환하는 함수"""
    try:

        def clean_text(text):
            if isinstance(text, dict):
                text = str(text)
            if isinstance(text, str):
                cleaned = (
                    text.replace("{", "")
                    .replace("}", "")
                    .replace("'", "")
                    .replace('"', "")
                )
                return cleaned.strip()
            return ""

        result = json.loads(raw_response.choices[0].message.content)

        # 각 섹션별 데이터 추출
        market_analysis = result.get("market_analysis", {})
        portfolio_analysis = result.get("portfolio_analysis", {})
        risk_analysis = result.get("risk_analysis", {})

        standardized_data = {
            "market_analysis": {
                "current_trends": {
                    "economic_indicators": clean_text(
                        market_analysis.get("current_trends", {}).get(
                            "economic_indicators"
                        )
                    ),
                    "sector_analysis": clean_text(
                        market_analysis.get("current_trends", {}).get("sector_analysis")
                    ),
                    "market_sentiment": clean_text(
                        market_analysis.get("current_trends", {}).get(
                            "market_sentiment"
                        )
                    ),
                },
                "global_impact": {
                    "macro_factors": clean_text(
                        market_analysis.get("global_impact", {}).get("macro_factors")
                    ),
                    "geopolitical_risks": clean_text(
                        market_analysis.get("global_impact", {}).get(
                            "geopolitical_risks"
                        )
                    ),
                    "currency_effects": clean_text(
                        market_analysis.get("global_impact", {}).get("currency_effects")
                    ),
                },
            },
            "portfolio_analysis": {
                "performance": {
                    "absolute_returns": clean_text(
                        portfolio_analysis.get("performance", {}).get(
                            "absolute_returns"
                        )
                    ),
                    "relative_returns": clean_text(
                        portfolio_analysis.get("performance", {}).get(
                            "relative_returns"
                        )
                    ),
                    "risk_adjusted_returns": clean_text(
                        portfolio_analysis.get("performance", {}).get(
                            "risk_adjusted_returns"
                        )
                    ),
                },
                "risk_metrics": {
                    "variance": clean_text(
                        portfolio_analysis.get("risk_metrics", {}).get("variance")
                    ),
                    "correlation": clean_text(
                        portfolio_analysis.get("risk_metrics", {}).get("correlation")
                    ),
                    "beta": clean_text(
                        portfolio_analysis.get("risk_metrics", {}).get("beta")
                    ),
                    "var": clean_text(
                        portfolio_analysis.get("risk_metrics", {}).get("var")
                    ),
                    "stress_test": clean_text(
                        portfolio_analysis.get("risk_metrics", {}).get("stress_test")
                    ),
                },
                "recommendation": {
                    "asset_allocation": clean_text(
                        portfolio_analysis.get("recommendation", {}).get(
                            "asset_allocation"
                        )
                    ),
                    "rebalancing": clean_text(
                        portfolio_analysis.get("recommendation", {}).get("rebalancing")
                    ),
                    "risk_management": clean_text(
                        portfolio_analysis.get("recommendation", {}).get(
                            "risk_management"
                        )
                    ),
                },
            },
            "risk_analysis": {
                "market_risks": {
                    "systematic_risk": clean_text(
                        risk_analysis.get("market_risks", {}).get("systematic_risk")
                    ),
                    "interest_rate_risk": clean_text(
                        risk_analysis.get("market_risks", {}).get("interest_rate_risk")
                    ),
                    "liquidity_risk": clean_text(
                        risk_analysis.get("market_risks", {}).get("liquidity_risk")
                    ),
                },
                "portfolio_risks": {
                    "concentration_risk": clean_text(
                        risk_analysis.get("portfolio_risks", {}).get(
                            "concentration_risk"
                        )
                    ),
                    "currency_risk": clean_text(
                        risk_analysis.get("portfolio_risks", {}).get("currency_risk")
                    ),
                    "credit_risk": clean_text(
                        risk_analysis.get("portfolio_risks", {}).get("credit_risk")
                    ),
                },
            },
        }

        return standardized_data

    except Exception as e:
        logger.error(f"응답 데이터 표준화 중 오류 발생: {str(e)}")
        return {"error": str(e)}
