#README

## I. 팀원 정보 및 업무 분담 내역

**김순도**
### API
- 금융감독원 API 연동 
- SerpAPI API 연동
- 한국투자증권 API 연동
- OpenAI API 연동

### 데이터 처리 및 분석
- 은행 예금 데이터 수집
- ETF 자산 데이터 전처리 및 DB 저장
- 구글 뉴스 기사 스크랩(KR, US) 및 연동
- ETF 종목별 5년 주가데이터 수집
- 최소분산포트폴리오 구현
- 현대포트폴리오 이론 적용(공분산 활용, Random Matrix Theory)
- Investing.com 패키지 활용, 주요국 경제 지표 수집

### 페이지 구현
- 메인페이지 제작
- 로그인페이지 제작
- 선호자산 페이지 제작
- 자산분석 페이지 제작
- AI 분석 페이지 제작

**정유진**
### API
- 사용자 인증 시스템 구현 (토큰 기반)
- 한국수출입은행 API 연동
- 카카오맵 API 연동

### 데이터 처리 및 분석
- 환율 계산기 제작

### 페이지 구현
- 회원가입 로그인 필드 확장
- 메인페이지 제작
- 회원 약관 동의 페이지 제작
- 프로필 페이지 제작
- 프로필 수정 페이지 제작
- 소개 페이지 제작
- 환율 계산 페이지 제작
- 투자성향측정 설문 페이지 제작
- 게시판 페이지 제작
- 주변 은행 찾기 페이지 제작


## II. 설계 내용 및 실제 구현 정도

### API 명세서
![API 명세서](https://github.com/user-attachments/assets/d37c3fd5-9b98-4c06-8918-66f985d8f387)

### 시스템 아키텍처
![아키텍처](https://github.com/user-attachments/assets/ff2f595e-ce1b-4a1a-a61b-cffe7101623a)

## III. 데이터베이스 모델링(ERD)
![ERD](https://github.com/user-attachments/assets/91727f37-5ca8-4b7e-8f95-c025c5d3ff3d)

## IV. 금융 상품 추천 알고리즘에 대한 기술적 설명

1. 사용자 선호 자산 선택
2. 선호 자산 기반으로 최소분산포트폴리오 구현
    - RMT 필터링
        - 노이즈와 실제 정보를 구분하는 임계값 계산
        - 노이즈를 제거하고 유의미한 상관관계만 추출
        - 공분산 행렬을 안정화하기 위한 정규화 적용
    - 포트폴리오 최적화
        - 연간 수익률 계산
        - 공분산 행렬 계산 및 필터링
        - 변동성 계산+
        - 제약 조건
            - 각 자산 비중 최대 30% 제한
            - 전체 비중의 합 100%
        - 무위험 수익률
            - 3.25% 한국은행 기준 금리 (2024.11.26 기준)
            - VaR 95% 위험 수준
3. 자산 상관관계, 위험도, 샤프비율, 기대수익률 제시
4. AI 분석
    - 분석 자료
        - 주요국 경제 지표 AI 분석
        - 한국, 미국 경제 뉴스 감정 평가 후 AI 분석
        - 최소분산포트폴리오 분석
    - 분석 내용 종합 평가

## V. 서비스 대표 기능들에 대한 설명

### LOGIN
![Login](https://github.com/user-attachments/assets/01b2a68c-ecdf-4b94-ad04-e4bfa40dfbec)

### SIGNUP
![SignUp](https://github.com/user-attachments/assets/34cf7149-93b5-4a36-ac62-382858d2aad1)

### ABOUT
![About](https://github.com/user-attachments/assets/9a271614-450f-4c8e-b36a-3f982a85f973)

### PROFILE
![Profile](https://github.com/user-attachments/assets/bcdcc3f6-1636-4cf1-be4f-b4b0558fc49f)

### PORTFOLIO
![portfolio](https://github.com/user-attachments/assets/f9650f96-0583-4839-8256-309031b7686c)

## VI. 생성형 AI를 활용한 부분

AI 분석
- 분석 자료
    - 주요국 경제 지표 AI 분석
    - 한국, 미국 경제 뉴스 감정 평가 후 AI 분석
    - 최소분산포트폴리오 분석
- 분석 결과
    - 시장 분석
        - 경제 지표
        - 섹터 분석
        - 시장 심리
    - 글로벌 영향
        - 거시경제 요인
        - 지정학적 리스크
        - 환율 영향
    - 포트폴리오 분석
        - 절대 수익률 분석
        - 상대 수익률 분석
        - 위험조정 수익률 분석
    - 리스크 지표
        - 변동성
        - 상관관계
        - 베타
        - VaR
        - 스트레스 테스트
    - 투자 추천
        - 자산 배분
        - 리밸런싱
        - 리스크 관리
- 리스크 분석
    - 시장 리스크
        - 시스템적 리스크 평가
        - 금리 리스크 평가
        - 유동성 리스크 평가
    - 포트폴리오 리스크
        - 집중 위험 평가
        - 환위험 평가
        - 신용위험 평가

### 프롬프트 (응답 데이터 표준화)

```
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
```

## VII. 기타(느낀 점, 후기 등)

Alchemist 프로젝트는 김순도, 정유진 두 명으로 구성되어 있으며, 각자의 역량을 살려 업무를 분담했습니다.

프로젝트의 주요 기능은 금융 데이터 수집과 처리에 중점을 두었습니다. 금융감독원 API를 활용하여 은행 예금 정보를 수집하고, Investing.com 패키지로 경제 지표를 분석했습니다. 또한 SerpAPI, 한국투자증권 API를 연동하여 다양한 금융 데이터를 확보했습니다. 투자론의 최소 분산 포트폴리오 이론을 활용한 기본 분석 시스템으로 최소분산포트폴리오도 구현했습니다. 추가로 OpenAI API를 활용하여 구성된 포트폴리오의 적합성과 리스크를 분석하였습니다.

프론트엔드 부분은 가능한 사용자 친화적인 환경을 조성하였고 토큰 기반의 인증 시스템을 구축하고, 프로필 페이지와 어바웃 페이지를 개발했습니다. 또한 메인페이지와 네비게이션 바를 구현하고, 회원가입 기능을 확장했습니다.

개발을 진행하면서 매일 새로운 도전과 배움의 기회가 있었습니다. API 데이터를 크롤링하고 처리하는 과정에서 여러 기술적 어려움을 겪었지만, 이를 해결하며 성장할 수 있었습니다. 특히 데이터 전처리와 DB 저장 과정에서의 복잡성을 체감했고, 안정적인 시스템 구축의 중요성을 깨달았습니다.

앞으로도 기능을 보완하며 더 나은 서비스를 만들기 위해 노력하겠습니다. 특히 ETF 데이터 처리와 경제 지표 연동에 집중하여 사용자들에게 유용한 금융 정보를 제공하고자 합니다.
