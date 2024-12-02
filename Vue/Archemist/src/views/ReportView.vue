<template>
  <div class="report-container">    
    <div v-if="loading" class="loading">
      데이터를 분석중입니다...
    </div>
    
    <div v-else-if="stockData" class="analysis-content">
      <h2>포트폴리오 분석 리포트</h2>
      <!-- 최적 포트폴리오 섹션 -->
      <section class="portfolio-section">
        <h3>최적 포트폴리오 구성</h3>
        <div class="portfolio-metrics">
          <div class="metric">
            <span class="label">포트폴리오 기대수익률:</span>
            <span class="value">{{ calculatePortfolioReturn(analysis.optimal_weights, analysis.returns) }}%</span>
          </div>
          <div class="metric">
            <span class="label">포트폴리오 샤프비율:</span>
            <span class="value">{{ calculatePortfolioSharpe() }}</span>
          </div>
          <div class="metric">
            <span class="label">포트폴리오 분산:</span>
            <span class="value">{{ Number(analysis.portfolio_variance).toFixed(4) }}</span>
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th>종목명</th>
              <th>비중</th>
              <th>기대수익률</th>
              <th>샤프비율</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(weight, index) in analysis.optimal_weights" :key="index">
              <td>{{ getEtfName(Object.keys(stockData)[index]) }}</td>
              <td>{{ (weight * 100).toFixed(2) }}%</td>
              <td>{{ (analysis.returns[Object.keys(stockData)[index]] * 100).toFixed(2) }}%</td>
              <td>{{ Number(analysis.sharpe_ratios[Object.keys(stockData)[index]]).toFixed(3) }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- 상관관계 분석 -->
      <section class="correlation-section">
        <h3>자산 간 상관관계</h3>
        <div class="correlation-matrix">
          <table>
            <thead>
              <tr>
                <th>종목</th>
                <th v-for="code in Object.keys(analysis.correlation)" :key="code">
                  {{ getEtfName(code) }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, code1) in analysis.correlation" :key="code1">
                <td>{{ getEtfName(code1) }}</td>
                <td v-for="(value, code2) in row" :key="code2" :class="getCorrelationClass(value)">
                  {{ Number(value).toFixed(3) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 개별 자산 분석 -->
      <section class="asset-analysis-section">
        <h3>개별 자산 분석</h3>
        <table>
          <thead>
            <tr>
              <th>종목명</th>
              <th>기대수익률</th>
              <th>샤프비율</th>
              <th>VaR (95%)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, code) in analysis.returns" :key="code">
              <td>{{ getEtfName(code) }}</td>
              <td>{{ (Number(value) * 100).toFixed(2) }}%</td>
              <td>{{ Number(analysis.sharpe_ratios[code]).toFixed(3) }}</td>
              <td>{{ (Number(analysis.var[code]) * 100).toFixed(2) }}%</td>
            </tr>
          </tbody>
        </table>
      </section>
      <div class="report-container">
        <!-- 기존 템플릿 내용 -->
        <button @click="sendToAiAnalysis" 
                class="analysis-button">
          AI 분석 요청
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { usePreferStore } from '@/stores/prefer'
import { useRouter } from 'vue-router'
import { useAiStore } from '@/stores/ai'


const router = useRouter()
const preferstore = usePreferStore()
const aiStore = useAiStore()
const loading = ref(false)
const stockData = ref(null)
const analysis = ref(null)

const etfNameCache = new Map();

const getEtfName = (code) => {
  if (etfNameCache.has(code)) {
    return etfNameCache.get(code);
  }
  const etf = preferstore.etfList.find(etf => etf.short_code === code);
  const name = etf ? etf.name : code;
  etfNameCache.set(code, name);
  return name;
};

const calculatePortfolioReturn = (weights, returns) => {
  if (!weights || !returns) return '0.00'
  return (weights.reduce((sum, weight, index) => {
    const code = Object.keys(returns)[index]
    return sum + weight * returns[code]
  }, 0) * 100).toFixed(2)
}

const calculatePortfolioSharpe = () => {
  if (!analysis.value) return '0.000'
  const riskFreeRate = 0.0325  // 한국 기준금리 3.25%
  const portfolioReturn = parseFloat(calculatePortfolioReturn(
    analysis.value.optimal_weights,
    analysis.value.returns
  )) / 100
  const portfolioStd = Math.sqrt(analysis.value.portfolio_variance)
  return ((portfolioReturn - riskFreeRate) / portfolioStd).toFixed(3)
}

const getCorrelationClass = (value) => {
  const val = Number(value)
  if (val > 0.7) return 'high-correlation'
  if (val < -0.7) return 'negative-correlation'
  return ''
}

const fetchStockData = async () => {
  try {
    loading.value = true;
    if (!preferstore.getSelectedShortCodes.length) {
      throw new Error('선택된 ETF가 없습니다.');
    }
    const response = await axios.post('http://localhost:8000/stock/stock-data/', {
      codes: preferstore.getSelectedShortCodes
    });
    if (!response.data || !response.data.data) {
      throw new Error('유효하지 않은 응답 데이터');
    }
    stockData.value = response.data.data;
    analysis.value = response.data.analysis;
  } catch (error) {
    console.error('데이터 조회 실패:', error);
    // 사용자에게 오류 메시지 표시 로직 추가
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  if (!preferstore.etfList.length) {
    await preferstore.fetchEtfList()
  }
  console.log('ETF 목록:', preferstore.etfList)
  console.log('선택된 코드:', preferstore.getSelectedShortCodes)
  fetchStockData()
})


const sendToAiAnalysis = async () => {
  try {
    // 데이터 유효성 검사
    if (!analysis.value || !stockData.value) {
      throw new Error('분석할 포트폴리오 데이터가 없습니다.');
    }

    loading.value = true;
    const portfolioData = {
      optimal_weights: analysis.value.optimal_weights,
      returns: analysis.value.returns,
      sharpe_ratios: analysis.value.sharpe_ratios,
      portfolio_variance: analysis.value.portfolio_variance,
      correlation: analysis.value.correlation,
      var: analysis.value.var,
      etf_names: Object.keys(stockData.value).map(code => ({
        code,
        name: getEtfName(code)
      }))
    };

    // 필수 데이터 검증
    const requiredFields = ['optimal_weights', 'returns', 'sharpe_ratios'];
    for (const field of requiredFields) {
      if (!portfolioData[field]) {
        throw new Error(`필수 데이터 ${field}가 누락되었습니다.`);
      }
    }

    const response = await axios.post(
      'http://localhost:8000/ai_analysis/analysis/',
      portfolioData,
      {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 300000, // 5분 타임아웃
        validateStatus: function (status) {
          return status >= 200 && status < 300;
        }
      }
    );

    if (response.data) {
      aiStore.setAnalysisResult(response.data);
      router.push({ name: 'AiReport' });
    }
  } catch (error) {
    console.error('AI 분석 요청 실패:', error.response?.data || error.message);
    // 에러 메시지 표시
    alert(error.response?.data?.error || error.message || 'AI 분석 중 오류가 발생했습니다.');
  } finally {
    loading.value = false;
  }
};

watch(() => preferstore.selectedShortCodes, (newValue) => {
  selectedAssets.value = [...newValue];
}, { deep: true });

</script>

<style scoped>
h2 {
  padding-bottom: 2rem;
}

.report-container {
  display: flex;
  justify-content: center;
  padding: 3rem;
  max-width: 75rem; /* 1200px -> 75rem */
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 2.5rem; /* 40px -> 2.5rem */
}

.portfolio-metrics {
  display: flex;
  gap: 2rem; /* 32px -> 2rem */
  margin: 1rem 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem; /* 8px -> 0.5rem */
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* 8px -> 0.5rem */
}

.label {
  font-weight: bold;
  color: #666;
}

.value {
  font-size: 1.2rem;
  color: #333;
}

section {
  margin-bottom: 1.875rem; /* 30px -> 1.875rem */
  padding: 1.25rem; /* 20px -> 1.25rem */
  border: 1px solid #ddd;
  border-radius: 0.5rem; /* 8px -> 0.5rem */
  background-color: white;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.9375rem; /* 15px -> 0.9375rem */
}

th,
td {
  padding: 0.75rem; /* 12px -> 0.75rem */
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.high-correlation {
  background-color: #ffebee;
}

.negative-correlation {
  background-color: #e8f5e9;
}

h3 {
  color: #333;
  margin-bottom: 0.9375rem; /* 15px -> 0.9375rem */
}

.analysis-button {
  width: 13rem; /* 13rem 그대로 */
  height: 3rem; /* 3rem 그대로 */
  padding: 0.75rem; /* 12px -> 0.75rem */
  margin-top: 1.25rem; /* 20px -> 1.25rem */
  padding: 0.625rem 1.25rem; /* 10px 20px -> 0.625rem 1.25rem */
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 0.625rem; /* 10px -> 0.625rem */
  cursor: pointer;
  font-size: 1rem; /* 16px -> 1rem */
}

.analysis-button:hover {
  background-color: #45a049;
}
</style>
