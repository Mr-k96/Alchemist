<template>
    <div class="exchange-rate">
      <h1>환율 계산기</h1>
  
      <!-- 계산기 영역 -->
      <div class="calculator">
        <input v-model.number="amount" type="number" placeholder="금액 입력" />
        <select v-model="targetCurrency">
          <option v-for="rate in exchangeRates" :key="rate.cur_unit" :value="rate.cur_unit">
            {{ rate.cur_unit }} ({{ rate.cur_nm }})
          </option>
        </select>
        <span class="to-text">to</span>
        <select v-model="baseCurrency">
          <option v-for="rate in exchangeRates" :key="rate.cur_unit" :value="rate.cur_unit">
            {{ rate.cur_unit }} ({{ rate.cur_nm }})
          </option>
        </select>
        <button @click="calculateRate">계산</button>
      </div>
  
      <!-- 결과 출력 -->
      <div v-if="result !== null" class="result">
        {{ amount }} {{ targetCurrency }} = {{ result }} {{ baseCurrency }}
      </div>
      <div v-if="error" class="error">
        {{ error }}
      </div>
  
      <!-- 계산 기록 -->
      <div v-if="history.length > 0" class="history">
        <h3>환율 계산 기록</h3>
        <ul>
          <li v-for="(record, index) in history" :key="index">
            {{ record.amount }} {{ record.target }} → {{ record.result }} {{ record.base }}
            <button class="delete-button" @click="deleteRecord(index)">X</button>
          </li>
        </ul>
      </div>
  
      <!-- 통화 정보 -->
      <div class="currency-info">
        <h2>통화 정보</h2>
        <select v-model="selectedCountry">
          <option v-for="rate in exchangeRates" :key="rate.cur_unit" :value="rate.cur_unit">
            {{ rate.cur_nm }}
          </option>
        </select>
        <div v-if="selectedCurrency" class="selected-info">
          <div class="flag" v-if="flags[selectedCurrency.cur_unit]">
            <img :src="flags[selectedCurrency.cur_unit]" alt="국기" />
          </div>
          <h3>선택한 통화 정보</h3>
          <p><strong>통화 단위:</strong> {{ selectedCurrency.cur_unit }}</p>
          <p><strong>통화 이름:</strong> {{ selectedCurrency.cur_nm }}</p>
          <p><strong>기준 환율:</strong> {{ selectedCurrency.deal_bas_r }}</p>
          <p><strong>송금 받으실 때:</strong> {{ selectedCurrency.ttb }}</p>
          <p><strong>송금 보내실 때:</strong> {{ selectedCurrency.tts }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from "vue";
  import { useExchangeRateStore } from "@/stores/exchange_rate";
  
  // 스토어 및 상태 정의
  const store = useExchangeRateStore();
  const amount = ref(1);
  const baseCurrency = ref("KRW");
  const targetCurrency = ref("USD");
  const result = ref(null);
  const error = ref(null);
  const exchangeRates = ref([]);
  const history = ref(JSON.parse(localStorage.getItem("exchangeHistory")) || []);
  const selectedCountry = ref(null);
  
  // 국기 URL 매핑
  const flags = {
    USD: "https://flagcdn.com/us.svg",
    KRW: "https://flagcdn.com/kr.svg",
    EUR: "https://flagcdn.com/eu.svg",
    JPY: "https://flagcdn.com/jp.svg",
    CNY: "https://flagcdn.com/cn.svg",
  };
  
  // 선택한 통화 정보
  const selectedCurrency = computed(() => {
    return exchangeRates.value.find((rate) => rate.cur_unit === selectedCountry.value);
  });
  
  // 환율 데이터 로드
  const loadExchangeRates = async () => {
    try {
      exchangeRates.value = await store.fetchExchangeRates();
      if (exchangeRates.value.length > 0) {
        selectedCountry.value = exchangeRates.value[0].cur_unit;
      }
    } catch (err) {
      console.error("환율 데이터를 가져오는 중 오류 발생:", err);
      error.value = "환율 데이터를 가져오는 데 실패했습니다.";
    }
  };
  
  // 환율 계산
  const calculateRate = () => {
    error.value = null;
    result.value = null;
  
    if (isNaN(amount.value) || amount.value <= 0) {
      error.value = "올바른 금액을 입력해주세요.";
      return;
    }
  
    const baseRate = exchangeRates.value.find((rate) => rate.cur_unit === baseCurrency.value);
    const targetRate = exchangeRates.value.find((rate) => rate.cur_unit === targetCurrency.value);
  
    if (!baseRate || !targetRate) {
      error.value = "유효하지 않은 통화를 선택하셨습니다.";
      return;
    }
  
    const baseRateValue = parseFloat(baseRate.deal_bas_r.replace(",", ""));
    const targetRateValue = parseFloat(targetRate.deal_bas_r.replace(",", ""));
  
    if (isNaN(baseRateValue) || isNaN(targetRateValue)) {
      error.value = "환율 데이터가 유효하지 않습니다.";
      return;
    }
  
    result.value = ((amount.value / baseRateValue) * targetRateValue).toFixed(2);
  
    // 계산 기록 저장
    const record = {
      amount: amount.value,
      target: targetCurrency.value,
      base: baseCurrency.value,
      result: result.value,
    };
    history.value.push(record);
    localStorage.setItem("exchangeHistory", JSON.stringify(history.value));
  };
  
  // 계산 기록 삭제
  const deleteRecord = (index) => {
    history.value.splice(index, 1);
    localStorage.setItem("exchangeHistory", JSON.stringify(history.value));
  };
  
  onMounted(() => {
    loadExchangeRates();
  });
  </script>
  
  <style scoped>
  /* 환율 계산기 전체 컨테이너 */
  .exchange-rate {
    max-width: 80rem; /* 900px -> 56.25rem */
    margin: 3rem auto; /* 중앙 정렬 및 여백 */
    padding: 2.5rem; /* 내부 여백 */
    background-color: #fefefe; /* 밝은 배경 */
    border-radius: 1rem; /* 둥근 테두리 */
    box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.05); /* 은은한 그림자 */
    font-family: 'GowunBatang-Regular', sans-serif; /* 기본 글씨체 */
    
  }
  
  /* 제목 스타일 */
  h1 {
    font-size: 2rem; /* 36px -> 2.25rem */
    font-weight: bold;
    color: #333333;
    font-family: 'DoHyeon-Regular', sans-serif; /* 강조된 글씨체 */
    margin-bottom: 2rem;
  }
  
  /* 계산기 섹션 */
  .calculator {
  display: flex;
  gap: 1rem; /* 요소 간의 간격 */
  margin-bottom: 4rem; /* 아래 여백 */
  margin-top: 4rem;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
}
  
  input,
  select,
  button {
    padding: 0.75rem 1rem; /* 10px -> 0.75rem */
    font-size: 1rem; /* 14px -> 1rem */
    border-radius: 0.375rem; /* 6px -> 0.375rem */
    border: 1px solid #ccc; /* 기본 테두리 */
  }
  
  /* 버튼 스타일 */
  button {
    background-color: #a8dadc; /* 버튼 배경 */
    color: white;
    border: none;
    cursor: pointer;
    font-family: 'DoHyeon-Regular', sans-serif;
    transition: background-color 0.2s ease, transform 0.2s ease; /* 부드러운 효과 */
  }
  
  button:hover {
    background-color: #457b9d; /* 호버 시 더 진한 색상 */
    transform: scale(1.05); /* 살짝 확대 효과 */
  }
  
  /* 통화 정보 섹션 */
  .currency-info {
    margin-top: 2rem; /* 20px -> 2rem */
    background: #fafafa; /* 연한 배경 */
    padding: 1.5rem; /* 15px -> 1.5rem */
    border-radius: 0.5rem;
    border: 0.0625rem solid #e0e0e0; /* 은은한 테두리 */
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.03); /* 가벼운 그림자 */
  }
  
  /* 선택한 통화 정보 텍스트 */
  .selected-info {
    text-align: left;
    font-size: 1rem; /* 14px -> 1rem */
    line-height: 2.5rem; /* 읽기 편한 줄 간격 */
  }
  
  .selected-info .flag img {
    width: 2.5rem; /* 40px -> 2.5rem */
    height: 1.5625rem; /* 25px -> 1.5625rem */
    margin-bottom: 0.625rem; /* 10px -> 0.625rem */
    border-radius: 0.25rem; /* 국기 이미지에 둥근 테두리 */
    box-shadow: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.1); /* 그림자 */
  }
  
  /* 계산 기록 섹션 */
  .history ul {
    list-style: none;
    padding: 0;
    margin-top: 2rem;
    margin-bottom: 4rem;
  }
  
  .history li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0; /* 5px -> 0.5rem */
    border-bottom: 0.0625rem solid #ddd; /* 은은한 구분선 */
  }

  
  /* 삭제 버튼 */
  .delete-button {
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 0.375rem;
    padding: 0.5rem; /* 5px -> 0.5rem */
    cursor: pointer;
    font-size: 0.875rem; /* 12px -> 0.875rem */
    transition: background-color 0.2s ease;
  }
  
  .delete-button:hover {
    background-color: #a71d2a; /* 어두운 빨간색 */
  }
  
  /* 결과 및 에러 메시지 */
  .result {
    font-size: 1.125rem; /* 18px -> 1.125rem */
    font-weight: bold;
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 4rem;
    color: #333;
  }
  
  .error {
    color: #ff4d4f; /* 에러 빨간색 */
    font-weight: bold;
    text-align: center;
    margin-top: 1rem;
  }
  </style>
  
  