import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def calculate_correlation_matrix(price_data):
    """주가 데이터로부터 상관관계 행렬을 계산하고 시각화하는 함수"""
    # 일간 수익률 계산
    returns = price_data.pct_change().dropna()
    
    # 상관관계 행렬 계산
    correlation_matrix = returns.corr()
    
    # 히트맵 생성
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, 
                annot=True,  # 숫자 표시
                cmap='coolwarm',  # 색상 맵
                vmin=-1, vmax=1,  # 상관계수 범위
                center=0)  # 중앙값
    plt.title('Asset Correlation Heatmap')
    plt.tight_layout()
    
    return correlation_matrix

def calculate_portfolio_metrics(price_data):
    """포트폴리오 지표(수익률, 공분산)를 계산하는 함수"""
    # 일간 수익률 계산
    returns = price_data.pct_change().dropna()
    
    # 연간 기대수익률 계산 (252 거래일 기준)
    expected_returns = returns.mean() * 252
    
    # 공분산 행렬 계산 (연간)
    covariance_matrix = returns.cov() * 252
    
    return expected_returns, covariance_matrix

def calculate_portfolio_variance(weights, covariance_matrix):
    """포트폴리오 분산을 계산하는 함수"""
    return np.dot(weights.T, np.dot(covariance_matrix, weights))

def get_minimum_variance_portfolio(expected_returns, covariance_matrix):
    """최소분산 포트폴리오의 가중치를 계산하는 함수"""
    num_assets = len(expected_returns)
    
    constraints = (
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    )
    bounds = tuple((0, 1) for asset in range(num_assets))
    initial_weights = np.array([1.0/num_assets] * num_assets)
    
    result = minimize(
        calculate_portfolio_variance,
        initial_weights,
        args=(covariance_matrix,),
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    
    return result.x

# 예시 데이터 생성
np.random.seed(42)
dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='B')
assets = ['Stock A', 'Stock B', 'Stock C', 'Stock D']

# 가상의 주가 데이터 생성
price_data = pd.DataFrame(
    np.random.randn(len(dates), len(assets)).cumsum(axis=0) + 100,
    index=dates,
    columns=assets
)

# 상관관계 분석
correlation_matrix = calculate_correlation_matrix(price_data)

# 포트폴리오 지표 계산
expected_returns, covariance_matrix = calculate_portfolio_metrics(price_data)

# 최소분산 포트폴리오 계산
optimal_weights = get_minimum_variance_portfolio(expected_returns, covariance_matrix)

# 결과 출력
print("\n자산별 연간 기대수익률:")
for asset, ret in zip(assets, expected_returns):
    print(f"{asset}: {ret:.2%}")

print("\n최적 포트폴리오 가중치:")
for asset, weight in zip(assets, optimal_weights):
    print(f"{asset}: {weight:.2%}")

print(f"\n포트폴리오 분산: {calculate_portfolio_variance(optimal_weights, covariance_matrix):.4f}")

# 상관관계 행렬 출력
print("\n상관관계 행렬:")
print(correlation_matrix)
plt.show()