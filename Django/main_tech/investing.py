import investpy
from datetime import datetime, timedelta
import pandas as pd

def get_historical_economic_calendar(from_date, to_date, countries=None, importances=['high']):
    try:
        # 경제 캘린더 데이터 조회
        calendar = investpy.economic_calendar(
            from_date=from_date,
            to_date=to_date,
            countries=countries,
            importances=importances,
            time_zone=None,
            time_filter='time_only'
        )
        
        # importance가 None이 아닌 데이터만 필터링
        calendar = calendar[calendar['importance'].notna()]
        
        # 날짜순으로 정렬
        calendar = calendar.sort_values('date', ascending=False)
        
        # 필요한 컬럼만 선택하여 반환
        selected_columns = ['date', 'time', 'zone', 'event', 'importance', 'actual', 'forecast', 'previous']
        return calendar[selected_columns]
        
    except Exception as e:
        print(f"데이터 조회 중 오류 발생: {e}")
        return None

# 사용 예시
if __name__ == "__main__":
    # 날짜 설정
    end_date = datetime.now()
    start_date = end_date - timedelta(days=360)
    
    # 날짜 형식 변환 (dd/mm/yyyy)
    from_date = start_date.strftime('%d/%m/%Y')
    to_date = end_date.strftime('%d/%m/%Y')
    
    # 특정 국가의 주요 경제 지표만 조회
    calendar_data = get_historical_economic_calendar(
        from_date=from_date,
        to_date=to_date,
        countries=['united states', 'south korea', 'china', 'japan', 'europe'],
        importances=['high']
    )
    
    if calendar_data is not None:
        # 결과 출력 형식 설정
        pd.set_option('display.max_rows', None)  # 모든 행 표시
        pd.set_option('display.max_columns', None)  # 모든 열 표시
        pd.set_option('display.width', None)  # 출력 너비 제한 해제
        
        print("과거 주요 경제 지표:")
        print(calendar_data)