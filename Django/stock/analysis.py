import numpy as np
import pandas as pd
from scipy.optimize import minimize

def process_stock_data(stock_data):
    """주봉 데이터를 DataFrame으로 변환
    
    Args:
        stock_data (dict): 주식 데이터 딕셔너리
        
    Returns:
        DataFrame: 날짜별 주가 데이터
    """
    processed_data = {}
    
    for code, data in stock_data.items():
        weekly_data = data['daily_prices']['output']
        prices = {
            item['stck_bsop_date']: float(item['stck_clpr'])
            for item in weekly_data
        }
        processed_data[code] = prices
    
    df = pd.DataFrame(processed_data)
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    return df.sort_index()

def calculate_correlation(price_data):
    """자산 간 상관관계 계산
    Returns:
        DataFrame: 상관계수 행렬
    """
    returns = price_data.pct_change(fill_method=None).dropna()
    return returns.corr()

def calculate_eigenvalue_threshold(returns, q=3):
    """RMT에 따른 임계 고유값 계산"""
    T, N = returns.shape
    sigma = np.std(returns)
    lambda_max = sigma**2 * (1 + 1/q + 2*np.sqrt(1/q))
    lambda_min = sigma**2 * (1 + 1/q - 2*np.sqrt(1/q))
    return lambda_max, lambda_min

def apply_rmt_filter(cov_matrix, returns):
    """RMT 필터링 적용"""
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    T, N = returns.shape
    q = T/N
    
    lambda_max, lambda_min = calculate_eigenvalue_threshold(returns, q)
    
    filtered_eigenvalues = np.where(
        eigenvalues > lambda_max,
        eigenvalues,
        np.mean(eigenvalues[eigenvalues <= lambda_max])
    )
    
    filtered_cov = eigenvectors @ np.diag(filtered_eigenvalues) @ eigenvectors.T
    return filtered_cov

def shrink_covariance(sample_cov, shrinkage_factor=0.1):
    """공분산 행렬 정규화"""
    n = len(sample_cov)
    target = np.identity(n) * np.mean(np.diag(sample_cov))
    return (1 - shrinkage_factor) * sample_cov + shrinkage_factor * target

def calculate_portfolio_metrics(price_data, risk_free_rate=0.0325):
    """포트폴리오 지표 계산
    
    Args:
        price_data (DataFrame): 주가 데이터
        risk_free_rate (float): 무위험 수익률
        
    Returns:
        tuple: (연간수익률, 공분산행렬, 변동성)
    """
    returns = price_data.pct_change(fill_method=None).dropna()
    
    # 연간화된 수익률 계산
    annual_returns = returns.mean() * 52
    
    # 공분산 행렬 계산 및 필터링
    sample_cov = returns.cov() * 52
    filtered_cov = apply_rmt_filter(sample_cov.values, returns.values)
    shrunk_filtered_cov = shrink_covariance(filtered_cov, shrinkage_factor=0.1)
    
    volatility = returns.std() * np.sqrt(52)
    
    return annual_returns, pd.DataFrame(
        shrunk_filtered_cov,
        index=sample_cov.index,
        columns=sample_cov.columns
    ), volatility

def calculate_minimum_variance_portfolio(returns, cov_matrix):
    """최소분산포트폴리오 계산
    
    Args:
        returns (Series): 기대수익률
        cov_matrix (DataFrame): 공분산 행렬
        
    Returns:
        ndarray: 최적 포트폴리오 비중
    """
    # 기대수익률과 샤프비율이 모두 양수인 자산만 필터링
    risk_free_rate = 0.0325
    volatility = np.sqrt(np.diag(cov_matrix))
    sharpe_ratios = (returns - risk_free_rate) / volatility
    
    # 두 조건을 모두 만족하는 자산만 선택
    valid_mask = (returns > 0) & (sharpe_ratios > 0)
    
    if not valid_mask.any():
        raise ValueError("적절한 자산이 없습니다")
    
    # 필터링된 데이터만 사용
    filtered_returns = returns[valid_mask]
    filtered_cov = cov_matrix.loc[valid_mask, valid_mask]
    
    num_assets = len(filtered_returns)
    initial_weights = np.array([1/num_assets] * num_assets)
    
    # 최적화 수행
    result = minimize(
        lambda w: np.dot(w.T, np.dot(filtered_cov, w)),
        initial_weights,
        method='SLSQP',
        bounds=tuple((0, 0.3) for _ in range(num_assets)),
        constraints=[{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    )
    
    # 결과를 전체 자산 인덱스로 변환
    final_weights = pd.Series(0.0, index=returns.index)
    final_weights[filtered_returns.index] = result.x
    
    return final_weights.values

def analyze_portfolio(stock_data):
    """포트폴리오 분석 실행"""
    price_data = process_stock_data(stock_data)
    correlation = calculate_correlation(price_data)
    returns, cov_matrix, volatility = calculate_portfolio_metrics(price_data)
    
    # volatility 매개변수 제거하고 함수 호출
    optimal_weights = calculate_minimum_variance_portfolio(returns, cov_matrix)
    sharpe_ratios = calculate_sharpe_ratio(returns, volatility)
    
    returns_data = price_data.pct_change(fill_method=None).dropna()
    var_values = {col: calculate_var(returns_data[col]) for col in returns_data.columns}
    
    return {
        'correlation': correlation.to_dict(),
        'returns': returns.to_dict(),
        'optimal_weights': optimal_weights.tolist(),
        'sharpe_ratios': sharpe_ratios.to_dict(),
        'var': var_values,
        'portfolio_variance': float(
            np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights))
        )
    }

# 한국 기준 금리를 무위험 이자율로 사용
def calculate_sharpe_ratio(returns, volatility, risk_free_rate=0.0325):
    """샤프 비율 계산
    Args:
        returns (Series): 기대수익률
        volatility (Series): 변동성
        risk_free_rate (float): 무위험 수익률
    Returns:
        Series: 각 자산의 샤프 비율
    """
    return (returns - risk_free_rate) / volatility

def calculate_var(returns, confidence_level=0.95):
    """Value at Risk 계산
    Args:
        returns (Series): 수익률
        confidence_level (float): 신뢰수준
    Returns:
        float: VaR 값
    """
    return np.percentile(returns, (1 - confidence_level) * 100)

def analyze_portfolio(stock_data):
    """포트폴리오 분석 실행"""
    price_data = process_stock_data(stock_data)
    correlation = calculate_correlation(price_data)
    returns, cov_matrix, volatility = calculate_portfolio_metrics(price_data)
    optimal_weights = calculate_minimum_variance_portfolio(returns, cov_matrix)
    sharpe_ratios = calculate_sharpe_ratio(returns, volatility)
    
    returns_data = price_data.pct_change(fill_method=None).dropna()
    var_values = {col: calculate_var(returns_data[col]) for col in returns_data.columns}
    
    return {
        'correlation': correlation.to_dict(),
        'returns': returns.to_dict(),
        'optimal_weights': optimal_weights.tolist(),
        'sharpe_ratios': sharpe_ratios.to_dict(),
        'var': var_values,
        'portfolio_variance': float(
            np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights))
        )
    }