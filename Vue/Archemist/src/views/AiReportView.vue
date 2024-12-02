<template>
    <div class="ai-report-container">
        <div v-if="loading" class="loading">
            AI가 포트폴리오를 분석중입니다...
        </div>

        <div v-else-if="analysisResult" class="analysis-content">
            <h2>AI 포트폴리오 분석 리포트</h2>
            
            <!-- 시장 분석 섹션 -->
            <section class="analysis-section">
                <h3>시장 분석</h3>
                <div class="analysis-subsection">
                    <h4>현재 시장 동향</h4>
                    <div class="indicator-group">
                        <div class="indicator-item">
                            <h5>경제 지표</h5>
                            <p>{{ analysisResult.market_analysis.current_trends.economic_indicators }}</p>
                        </div>
                        <div class="indicator-item">
                            <h5>섹터 분석</h5>
                            <p>{{ analysisResult.market_analysis.current_trends.sector_analysis }}</p>
                        </div>
                        <div class="indicator-item">
                            <h5>시장 심리</h5>
                            <p>{{ analysisResult.market_analysis.current_trends.market_sentiment }}</p>
                        </div>
                    </div>
                </div>
                <div class="analysis-subsection">
                    <h4>글로벌 영향</h4>
                    <div class="indicator-group">
                        <div class="indicator-item">
                            <h5>거시경제 요인</h5>
                            <p>{{ analysisResult.market_analysis.global_impact.macro_factors }}</p>
                        </div>
                        <div class="indicator-item">
                            <h5>지정학적 리스크</h5>
                            <p>{{ analysisResult.market_analysis.global_impact.geopolitical_risks }}</p>
                        </div>
                        <div class="indicator-item">
                            <h5>환율 영향</h5>
                            <p>{{ analysisResult.market_analysis.global_impact.currency_effects }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 포트폴리오 분석 섹션 -->
            <section class="portfolio-section">
                <h3>포트폴리오 분석</h3>
                <div class="analysis-subsection">
                    <h4>성과 분석</h4>
                    <div class="performance-metrics">
                        <div class="metric-item">
                            <h5>절대 수익률</h5>
                            <p>{{ analysisResult.portfolio_analysis.performance.absolute_returns }}</p>
                        </div>
                        <div class="metric-item">
                            <h5>상대 수익률</h5>
                            <p>{{ analysisResult.portfolio_analysis.performance.relative_returns }}</p>
                        </div>
                        <div class="metric-item">
                            <h5>위험조정 수익률</h5>
                            <p>{{ analysisResult.portfolio_analysis.performance.risk_adjusted_returns }}</p>
                        </div>
                    </div>
                </div>
                <div class="analysis-subsection">
                    <h4>리스크 지표</h4>
                    <div class="risk-metrics">
                        <div class="metric-item">
                            <h5>변동성</h5>
                            <p>{{ analysisResult.portfolio_analysis.risk_metrics.variance }}</p>
                        </div>
                        <div class="metric-item">
                            <h5>상관관계</h5>
                            <p>{{ analysisResult.portfolio_analysis.risk_metrics.correlation }}</p>
                        </div>
                        <div class="metric-item">
                            <h5>베타</h5>
                            <p>{{ analysisResult.portfolio_analysis.risk_metrics.beta }}</p>
                        </div>
                        <div class="metric-item">
                            <h5>VaR</h5>
                            <p>{{ analysisResult.portfolio_analysis.risk_metrics.var }}</p>
                        </div>
                        <div class="metric-item">
                            <h5>스트레스 테스트</h5>
                            <p>{{ analysisResult.portfolio_analysis.risk_metrics.stress_test }}</p>
                        </div>
                    </div>
                </div>
                <div class="analysis-subsection">
                    <h4>투자 추천</h4>
                    <div class="recommendations">
                        <div class="recommendation-item">
                            <h5>자산 배분</h5>
                            <p>{{ analysisResult.portfolio_analysis.recommendation.asset_allocation }}</p>
                        </div>
                        <div class="recommendation-item">
                            <h5>리밸런싱</h5>
                            <p>{{ analysisResult.portfolio_analysis.recommendation.rebalancing }}</p>
                        </div>
                        <div class="recommendation-item">
                            <h5>리스크 관리</h5>
                            <p>{{ analysisResult.portfolio_analysis.recommendation.risk_management }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 리스크 분석 섹션 -->
            <section class="risk-section">
                <h3>리스크 분석</h3>
                <div class="risk-analysis">
                    <div class="risk-category">
                        <h4>시장 리스크</h4>
                        <div class="risk-items">
                            <div class="risk-item">
                                <h5>시스템적 리스크</h5>
                                <p>{{ analysisResult.risk_analysis.market_risks.systematic_risk }}</p>
                            </div>
                            <div class="risk-item">
                                <h5>금리 리스크</h5>
                                <p>{{ analysisResult.risk_analysis.market_risks.interest_rate_risk }}</p>
                            </div>
                            <div class="risk-item">
                                <h5>유동성 리스크</h5>
                                <p>{{ analysisResult.risk_analysis.market_risks.liquidity_risk }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="risk-category">
                        <h4>포트폴리오 리스크</h4>
                        <div class="risk-items">
                            <div class="risk-item">
                                <h5>집중 위험</h5>
                                <p>{{ analysisResult.risk_analysis.portfolio_risks.concentration_risk }}</p>
                            </div>
                            <div class="risk-item">
                                <h5>환위험</h5>
                                <p>{{ analysisResult.risk_analysis.portfolio_risks.currency_risk }}</p>
                            </div>
                            <div class="risk-item">
                                <h5>신용위험</h5>
                                <p>{{ analysisResult.risk_analysis.portfolio_risks.credit_risk }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAiStore } from '@/stores/ai'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(true)
const analysisResult = ref({
    market_analysis: {
        current_trends: {
            economic_indicators: '',
            sector_analysis: '',
            market_sentiment: ''
        },
        global_impact: {
            macro_factors: '',
            geopolitical_risks: '',
            currency_effects: ''
        }
    },
    portfolio_analysis: {
        performance: {
            absolute_returns: '',
            relative_returns: '',
            risk_adjusted_returns: ''
        },
        risk_metrics: {
            variance: '',
            correlation: '',
            beta: '',
            var: '',
            stress_test: ''
        },
        recommendation: {
            asset_allocation: '',
            rebalancing: '',
            risk_management: ''
        }
    },
    risk_analysis: {
        market_risks: {
            systematic_risk: '',
            interest_rate_risk: '',
            liquidity_risk: ''
        },
        portfolio_risks: {
            concentration_risk: '',
            currency_risk: '',
            credit_risk: ''
        }
    }
})

const aiStore = useAiStore()
const { analysisResult: storeResult } = storeToRefs(aiStore)

watch(storeResult, (newValue) => {
    try {
        if (newValue) {
            analysisResult.value = {
                ...analysisResult.value,
                ...JSON.parse(JSON.stringify(newValue))
            }
        }
        loading.value = false
    } catch (error) {
        console.error('데이터 처리 중 오류:', error)
        loading.value = false
    }
}, { immediate: true })

onMounted(() => {
    if (aiStore.analysisResult) {
        analysisResult.value = JSON.parse(JSON.stringify(aiStore.analysisResult))
        loading.value = false
        return
    }
    router.push({ name: 'Report' })
})
</script>

<style scoped>
.ai-report-container {
    padding: 1.25rem; /* 20px -> 1.25rem */
    max-width: 75rem; /* 1200px -> 75rem */
    margin: 0 auto;
}

.loading {
    text-align: center;
    padding: 2.5rem; /* 40px -> 2.5rem */
    font-size: 1.2rem; /* 그대로 1.2rem */
    color: #666;
}

.analysis-content {
    margin-top: 1.25rem; /* 20px -> 1.25rem */
}

section {
    margin-bottom: 1.875rem; /* 30px -> 1.875rem */
    padding: 1.5625rem; /* 25px -> 1.5625rem */
    border-radius: 0.75rem; /* 12px -> 0.75rem */
    box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1); /* 2px -> 0.125rem, 8px -> 0.5rem */
}

h2 {
    color: #2c3e50;
    margin-bottom: 1.875rem; /* 30px -> 1.875rem */
    font-size: 2rem; /* 그대로 2rem */
    text-align: center;
}

h3 {
    color: #2c3e50;
    margin-bottom: 1.25rem; /* 20px -> 1.25rem */
    font-size: 1.6rem; /* 그대로 1.6rem */
    border-bottom: 0.125rem solid #eee; /* 2px -> 0.125rem */
    padding-bottom: 0.625rem; /* 10px -> 0.625rem */
}

h4 {
    color: #34495e;
    margin: 0.9375rem 0; /* 15px -> 0.9375rem */
    font-size: 1.3rem; /* 그대로 1.3rem */
}

h5 {
    color: #455a64;
    margin: 0.625rem 0; /* 10px -> 0.625rem */
    font-size: 1.1rem; /* 그대로 1.1rem */
    font-weight: 600;
}

.analysis-subsection {
    margin-bottom: 1.5625rem; /* 25px -> 1.5625rem */
}

.indicator-group,
.performance-metrics,
.risk-metrics,
.recommendations,
.risk-items {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(15.625rem, 1fr)); /* 250px -> 15.625rem */
    gap: 1.25rem; /* 20px -> 1.25rem */
    margin-top: 0.9375rem; /* 15px -> 0.9375rem */
}

.indicator-item,
.metric-item,
.recommendation-item,
.risk-item {
    background-color: #fff;
    padding: 0.9375rem; /* 15px -> 0.9375rem */
    border-radius: 0.5rem; /* 8px -> 0.5rem */
    box-shadow: 0 0.0625rem 0.25rem rgba(0, 0, 0, 0.05); /* 1px -> 0.0625rem, 4px -> 0.25rem */
}

.analysis-section {
    background-color: #f8f9fa;
}

.portfolio-section {
    background-color: #fff;
}

.risk-section {
    background-color: #fff5f5;
}

.risk-category {
    margin-bottom: 1.25rem; /* 20px -> 1.25rem */
}

p {
    color: #596275;
    line-height: 1.6;
    margin: 0.5rem 0; /* 8px -> 0.5rem */
}

@media (max-width: 48rem) { /* 768px -> 48rem */
    .indicator-group,
    .performance-metrics,
    .risk-metrics,
    .recommendations,
    .risk-items {
        grid-template-columns: 1fr;
    }
}
</style>
