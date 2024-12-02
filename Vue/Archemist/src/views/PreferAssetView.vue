<template>
  <div class="portfolio-container">
    <!-- 첫 번째 줄: 사용자 정보 -->
    <div class="filter-row">
      <div class="user-info-group">
        <h3>투자자 정보</h3>
        <div class="user-info">
          <p>나의 투자 유형: {{ surveystore.investmentType }}</p>
          <p>나이: {{ userStore.userProfile ? calculateAge(userStore.userProfile.date_of_birth) : "로딩 중..." }}세</p>
        </div>
      </div>
    </div>

    <!-- 두 번째 줄: 기본 필터들 -->
    <div class="filter-row">
      <div class="filter-group">
        <h3>위험도</h3>
        <div class="checkbox-grid">
          <div v-for="riskGroup in riskGroups" :key="riskGroup.label" class="checkbox-item">
            <input type="checkbox" :value="riskGroup.value" v-model="selectedRiskGroups" @change="updateRiskFilters" />
            {{ riskGroup.label }}
          </div>
        </div>
      </div>

      <div class="filter-group">
        <h3>시장 분류</h3>
        <div class="checkbox-grid">
          <div v-for="market in marketOptions" :key="market" class="checkbox-item">
            <input type="checkbox" :value="market" v-model="selectedFilters.markets" @change="applyAllFilters" />
            {{ market }}
          </div>
        </div>
      </div>

      <div class="filter-group">
        <h3>자산 분류</h3>
        <div class="checkbox-grid">
          <div v-for="asset in assetOptions" :key="asset" class="checkbox-item">
            <input type="checkbox" :value="asset" v-model="selectedFilters.assets" @change="applyAllFilters" />
            {{ asset }}
          </div>
        </div>
      </div>

      <div class="filter-group">
        <h3>자산 옵션</h3>
        <div class="checkbox-grid">
          <div v-for="option in stockOptions" :key="option" class="checkbox-item">
            <input type="checkbox" :value="option" v-model="selectedFilters.stockOptions" @change="applyAllFilters" />
            {{ option }}
          </div>
        </div>
      </div>

      <div class="filter-group">
        <h3>채권 옵션</h3>
        <div class="checkbox-grid">
          <div v-for="option in bondOptions" :key="option" class="checkbox-item">
            <input type="checkbox" :value="option" v-model="selectedFilters.bondOptions" @change="applyAllFilters" />
            {{ option }}
          </div>
        </div>
      </div>
    </div>

    <!-- 세 번째 줄: 산업 분류 -->
    <div class="filter-row">
      <div class="industry-filter-group">
        <h3>산업 분류</h3>
        <div class="industry-categories">
          <div v-for="(industries, category) in industryCategories" :key="category" class="industry-category">
            <h4>{{ category }}</h4>
            <div v-for="industry in industries" :key="industry" class="industry-checkbox">
              <input type="checkbox" :value="industry" v-model="selectedFilters.industries" @change="applyAllFilters" />
              {{ industry }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="filter-row">
      <div class="selected-assets-group">
        <h3>선택된 자산</h3>
        <div class="selected-assets-table">
          <table>
            <thead>
              <tr>
                <th>선택</th>
                <th>종목명</th>
                <th>단축코드</th>
                <th>위험도</th>
                <th>자산분류</th>
                <th>산업분류</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="etf in selectedEtfList" :key="etf.short_code">
                <td>
                  <input type="checkbox" :checked="isSelected(etf)" @change="handleEtfSelection(etf)" />
                </td>
                <td>{{ etf.name }}</td>
                <td>{{ etf.short_code }}</td>
                <td>{{ etf.risk_level }}</td>
                <td>{{ etf.asset_category }}</td>
                <td>{{ getIndustries(etf) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="selected-count">
          선택된 자산 수: {{ selectedEtfList.length }}개
        </div>
      </div>
    </div>

    <div class="report-btn-container">
      <button class="report-btn" @click.prevent="goToReport">포트폴리오 만들기</button>
    </div>

    <div class="etf-list">
      <table>
        <thead>
          <tr>
            <th>선택</th>
            <th>종목명</th>
            <th>단축코드</th>
            <th>위험도</th>
            <th>운용사</th>
            <th>시장분류</th>
            <th>자산분류</th>
            <th>산업분류</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="etf in preferstore.etfList" :key="etf.short_code">
            <td>
              <input type="checkbox" :checked="isEtfSelected(etf)" @change="handleEtfSelection(etf)" />
            </td>
            <td>{{ etf.name }}</td>
            <td>{{ etf.short_code }}</td>
            <td>{{ etf.risk_level }}</td>
            <td>{{ etf.manager }}</td>
            <td>{{ etf.market_category }}</td>
            <td>{{ etf.asset_category }}</td>
            <td>{{ getIndustries(etf) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { usePreferStore } from "@/stores/prefer";
import { useCounterStore } from "@/stores/counter";
import { useSurveyStore } from "@/stores/survey";
import { useRouter } from 'vue-router'

const preferstore = usePreferStore();
const surveystore = useSurveyStore();
const userStore = useCounterStore();
const router = useRouter()

const selectedAssets = ref([]);
const selectedEtfList = ref([]); // 선택된 ETF 목록을 저장할 ref
const selectedRiskGroups = ref([]);

const riskGroups = [
  { label: '고위험', value: 'high', risks: ['1', '2'] },
  { label: '중위험', value: 'medium', risks: ['3', '4'] },
  { label: '저위험', value: 'low', risks: ['5', '6'] }
];
const marketOptions = ["국내", "해외", "국내&해외"];
const assetOptions = ["주식", "채권", "혼합자산", "원자재", "부동산", "기타"];
const stockOptions = ["배당주", "커버드콜", "환헷지"];
const bondOptions = ["국채", "회사채", "금융채", "통안채", "단기채", "특수채", "산금채", "중금채", "은행채"];
const industryCategories = {
  "기술/IT": ["AI", "IT", "IoT", "반도체", "소프트웨어", "보안"],
  "친환경/에너지": ["2차전지", "친환경", "에너지"],
  "바이오/헬스케어": ["바이오", "헬스케어", "의료기기"],
  "금융": ["은행", "증권", "금융채"],
  "소비재/서비스": ["소비재", "게임", "미디어컨텐츠", "여행레저", "화장품"],
  "산업/인프라": ["건설", "철강", "항공우주", "자동차", "인프라"],
  "디지털/플랫폼": ["메타버스", "플랫폼", "인터넷"],
  "ESG": ["ESG"]
};


const calculateAge = dateOfBirth => {
  if (!dateOfBirth) return "미설정";
  const today = new Date();
  const birthDate = new Date(dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
};

const selectedFilters = ref({
  risks: [],
  markets: [],
  assets: [],
  stockOptions: [],
  bondOptions: [],
  industries: []
});

const getIndustries = etf => {
  return [etf.industry_1, etf.industry_2, etf.industry_3, etf.industry_4]
    .filter(industry => industry)
    .join(", ");
};

const updateRiskFilters = () => {
  selectedFilters.value.risks = selectedRiskGroups.value.flatMap(group => {
    const riskGroup = riskGroups.find(r => r.value === group);
    return riskGroup ? riskGroup.risks : [];
  });
  applyAllFilters();
};

const saveAndCheckShortCodes = () => {
  preferstore.selectedShortCodes = selectedAssets.value;
  console.log('저장된 단축 코드 목록:', preferstore.getSelectedShortCodes);
};

const applyAllFilters = async () => {
  // 기본 필터 데이터
  let filterData = {
    risks: selectedFilters.value.risks,
    markets: selectedFilters.value.markets,
    assets: selectedFilters.value.assets,
    stock_options: [],
    bond_options: [],
    industries: []
  };

  // 자산별 필터 적용
  selectedFilters.value.assets.forEach(asset => {
    if (asset === '주식') {
      // 주식 자산에만 주식 옵션과 산업 분류 적용
      filterData.stock_options = selectedFilters.value.stockOptions;
      filterData.industries = selectedFilters.value.industries;
    }
    if (asset === '채권') {
      // 채권 자산에만 채권 옵션 적용
      filterData.bond_options = selectedFilters.value.bondOptions;
    }
  });

  // 필터 적용 및 결과 업데이트
  preferstore.filters = filterData;
  await preferstore.applyFilters();
  saveAndCheckShortCodes();
};

const isEtfSelected = (etf) => {
  return selectedAssets.value.includes(etf.short_code);
};

const isSelected = (etf) => {
  try {
    return selectedEtfList.value.some(item => item.short_code === etf.short_code);
  } catch (error) {
    console.error('체크박스 상태 확인 중 오류 발생:', error);
    return false;
  }
};

// ETF 선택 처리 함수
const handleEtfSelection = (etf) => {
  try {
    const index = selectedEtfList.value.findIndex(item => item.short_code === etf.short_code);
    if (index === -1) {
      // ETF가 선택되지 않은 경우 추가
      selectedEtfList.value.push(etf);
      if (!selectedAssets.value.includes(etf.short_code)) {
        selectedAssets.value.push(etf.short_code);
      }
    } else {
      // ETF가 이미 선택된 경우 제거
      selectedEtfList.value.splice(index, 1);
      const shortCodeIndex = selectedAssets.value.indexOf(etf.short_code);
      if (shortCodeIndex > -1) {
        selectedAssets.value.splice(shortCodeIndex, 1);
      }
    }
    // Pinia store 업데이트
    preferstore.selectedShortCodes = selectedAssets.value;
  } catch (error) {
    console.error('ETF 선택 처리 중 오류 발생:', error);
  }
};

onMounted(async () => {
  await preferstore.fetchEtfList();
  applyAllFilters();
  saveAndCheckShortCodes();
});

watch(selectedFilters, () => {
  applyAllFilters();
}, { deep: true });

const goToReport = async () => {
  await saveAndCheckShortCodes();
  router.push({ name: 'Report' });
};
</script>

<style scoped>
.portfolio-container {
  width: 56.25rem; /* 90rem -> 56.25rem */
  margin: auto;
  padding: 5rem; /* 5rem 그대로 */
}

/* 필터 컨테이너 스타일 */
.filters {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.25rem; /* 20px -> 1.25rem */
  margin-bottom: 1.25rem; /* 20px -> 1.25rem */
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem; /* 20px -> 1.25rem */
  padding: 0.9375rem; /* 15px -> 0.9375rem */
  border: 1px solid #eee;
  border-radius: 0.25rem; /* 4px -> 0.25rem */
  margin-bottom: 1.5rem; /* 24px -> 1.5rem */
}

.filter-group {
  flex: 1;
  min-width: 18.75rem; /* 300px -> 18.75rem */
  padding: 0.9375rem; /* 15px -> 0.9375rem */
  border: 1px solid #ddd;
  border-radius: 0.25rem; /* 4px -> 0.25rem */
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.625rem; /* 10px -> 0.625rem */
  margin-top: 0.625rem; /* 10px -> 0.625rem */
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.3125rem; /* 5px -> 0.3125rem */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.filter-group h3 {
  margin-bottom: 0.625rem; /* 10px -> 0.625rem */
}

.industry-filter-group {
  width: 100%;
  padding: 0.9375rem; /* 15px -> 0.9375rem */
  border: 1px solid #ddd;
  border-radius: 0.25rem; /* 4px -> 0.25rem */
}

.industry-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem; /* 10px -> 0.625rem */
  justify-content: flex-start;
}

.industry-category {
  flex: 0 1 calc(12.5% - 0.75rem); /* 12.5% - 12px -> 12.5% - 0.75rem */
  min-width: 8.75rem; /* 140px -> 8.75rem */
  border: 1px solid #eee;
  padding: 0.5rem; /* 8px -> 0.5rem */
  border-radius: 0.25rem; /* 4px -> 0.25rem */
}

.industry-category h4 {
  margin: 0 0 0.5rem 0; /* 8px -> 0.5rem */
  padding-bottom: 0.25rem; /* 4px -> 0.25rem */
  border-bottom: 1px solid #eee;
  font-size: 0.9rem; /* 그대로 0.9rem */
}

.industry-checkbox {
  display: flex;
  align-items: center;
  gap: 0.25rem; /* 4px -> 0.25rem */
  margin: 0.25rem 0; /* 4px -> 0.25rem */
  font-size: 0.85rem; /* 그대로 0.85rem */
}

/* 체크박스 컨테이너 스타일 */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.5rem; /* 8px -> 0.5rem */
  margin: 0.375rem 0; /* 6px -> 0.375rem */
}

/* 테이블 스타일 */
.etf-list {
  max-height: 31.25rem; /* 500px -> 31.25rem */
  overflow-y: auto;
  overflow-x: auto;
  margin-top: 1.25rem; /* 20px -> 1.25rem */
  border: 1px solid #eee;
  border-radius: 0.25rem; /* 4px -> 0.25rem */
}

.etf-list table {
  width: 100%;
  border-collapse: collapse;
}

.etf-list th {
  position: sticky;
  top: 0;
  background-color: #f8f9fa;
  z-index: 1;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 0.75rem; /* 12px -> 0.75rem */
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 500;
  position: sticky;
  top: 0;
}

/* 버튼 스타일 */
.report-btn-container {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0; /* 24px -> 1.5rem */
}

.report-btn {
  padding: 0.75rem 1.5rem; /* 12px 24px -> 0.75rem 1.5rem */
  background: #000;
  color: white;
  border: none;
  border-radius: 0.25rem; /* 4px -> 0.25rem */
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.report-btn:hover {
  background: #222;
}

.report-btn:active {
  transform: scale(0.98);
}

.selected-assets-group {
  width: 100%;
  padding: 0.9375rem; /* 15px -> 0.9375rem */
  border: 1px solid #ddd;
  border-radius: 0.25rem; /* 4px -> 0.25rem */
}

.selected-assets-table {
  margin-top: 0.9375rem; /* 15px -> 0.9375rem */
  overflow-x: auto;
}

.selected-assets-table table {
  width: 100%;
  border-collapse: collapse;
}

.selected-assets-table th,
.selected-assets-table td {
  padding: 0.625rem; /* 10px -> 0.625rem */
  text-align: left;
  border-bottom: 1px solid #eee;
}

.selected-assets-table th {
  background-color: #f8f9fa;
  font-weight: 500;
}

.selected-count {
  margin-top: 0.9375rem; /* 15px -> 0.9375rem */
  text-align: right;
  font-weight: 500;
}

@media screen and (max-width: 64rem) {  /* 1024px */
  .filter-group {
    min-width: calc(50% - 1.25rem); /* 50% - 20px -> 50% - 1.25rem */
  }
  
  .checkbox-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .industry-categories {
    grid-template-columns: repeat(auto-fill, minmax(12rem, 1fr)); /* 12rem -> 12rem */
  }
}

@media screen and (max-width: 48rem) {  /* 768px */
  .filter-group {
    min-width: 100%;
  }
  
  .checkbox-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 36rem) {  /* 576px */
  .checkbox-grid {
    grid-template-columns: 1fr;
  }
  
  .industry-categories {
    grid-template-columns: 1fr;
  }
}
</style>
