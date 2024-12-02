<script setup>
import { ref, onMounted, watch } from 'vue';
import { useEtfStore } from '@/stores/etf';

const etfStore = useEtfStore();
const searchTerm = ref('');

// 검색어 변경 감시
watch(searchTerm, (newValue) => {
  etfStore.searchAssets(newValue);
});

onMounted(async () => {
  await etfStore.fetchEtfData();
});
</script>

<template>
  <div class="asset-view">
    <h1>ETF 정보</h1>

    <!-- 검색 섹션 -->
    <div class="search-section">
      <input
        v-model="searchTerm"
        placeholder="ETF명 또는 운용사명 검색"
        class="search-input"
      />
    </div>

    <!-- 로딩 상태 표시 -->
    <div v-if="etfStore.loading" class="loading">
      데이터를 불러오는 중입니다...
    </div>

    <!-- 에러 메시지 표시 -->
    <div v-if="etfStore.error" class="error-message">
      {{ etfStore.error }}
    </div>

    <!-- ETF 상품 목록 -->
    <div v-if="!etfStore.loading && !etfStore.error" class="assets-container">
      <div
        v-for="asset in etfStore.filteredAssets"
        :key="asset.short_code"
        class="asset-card"
      >
        <div class="asset-header">
          <h3>{{ asset.name || 'ETF 이름 정보 없음' }}</h3>
          <span class="manager-name">{{ asset.manager || '운용사 정보 없음' }}</span>
        </div>

        <div class="asset-details">
          <p><strong>시장분류:</strong> {{ asset.market_category || '정보 없음' }}</p>
          <p><strong>자산분류:</strong> {{ asset.asset_category || '정보 없음' }}</p>
          <p><strong>위험도:</strong> {{ asset.risk_level || '정보 없음' }}</p>
          <div class="industry-info">
            <h4>산업 분류</h4>
            <p v-if="asset.industry_1">1차: {{ asset.industry_1 }}</p>
            <p v-if="asset.industry_2">2차: {{ asset.industry_2 }}</p>
            <p v-if="asset.industry_3">3차: {{ asset.industry_3 }}</p>
            <p v-if="asset.industry_4">4차: {{ asset.industry_4 }}</p>
            <p v-if="!asset.industry_1 && !asset.industry_2 && !asset.industry_3 && !asset.industry_4">
              산업 분류 정보가 없습니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.asset-view {
  max-width: 90rem; /* 최대 너비 설정 */
  margin: 3rem auto; /* 중앙 정렬 및 여백 */
  padding: 2rem; /* 내부 여백 */
  background-color: #ffffff; /* 배경색 */
  border-radius: 1rem; /* 둥근 테두리 */
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  font-family: 'Arial', sans-serif; /* 기본 글씨체 */
}

h1 {
  font-size: 2rem; /* 예금정보 제목 */
  font-weight: 600;
  color: #333;
  margin-bottom: 2rem; /* 아래 여백 */
  margin-left: 0.5rem;
  margin-top: 0.5rem;;
  text-align: left; /* 왼쪽 정렬 */
  letter-spacing: -0.5px; /* 자간 조정 */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* 세련된 폰트 */
}

.search-section {
  margin: 1.25rem 0; /* 20px -> 1.25rem */
}

.search-input {
  width: 100%;
  padding: 0.625rem; /* 10px -> 0.625rem */
  border: 1px solid #ddd;
  border-radius: 0.3125rem; /* 5px -> 0.3125rem */
  font-size: 1rem; /* 16px -> 1rem */
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #4a90e2;
  outline: none;
}

.assets-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(18.75rem, 1fr)); /* 300px -> 18.75rem */
  gap: 1.25rem; /* 20px -> 1.25rem */
}

.asset-card {
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem; /* 8px -> 0.5rem */
  padding: 0.9375rem; /* 15px -> 0.9375rem */
  background-color: white;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1); /* 2px -> 0.125rem, 4px -> 0.25rem */
  transition: transform 0.2s ease;
}

.asset-card:hover {
  transform: translateY(-0.125rem); /* 2px -> 0.125rem */
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.15); /* 4px -> 0.25rem, 8px -> 0.5rem */
}

.asset-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 0.625rem; /* 10px -> 0.625rem */
  margin-bottom: 0.625rem; /* 10px -> 0.625rem */
}

.asset-header h3 {
  margin: 0 0 0.3125rem 0; /* 5px -> 0.3125rem */
  color: #333;
}

.manager-name {
  font-size: 0.875rem; /* 0.9em -> 0.875rem */
  color: #666;
}

.loading,
.error-message {
  text-align: center;
  padding: 1.25rem; /* 20px -> 1.25rem */
  margin: 1.25rem 0; /* 20px -> 1.25rem */
  border-radius: 0.5rem; /* 8px -> 0.5rem */
}

.loading {
  background-color: #f8f9fa;
  color: #666;
}

.error-message {
  color: #dc3545;
  border: 1px solid #dc3545;
  background-color: #fff3f3;
}

.industry-info {
  margin-top: 0.625rem; /* 10px -> 0.625rem */
  padding-top: 0.625rem; /* 10px -> 0.625rem */
  border-top: 1px solid #eee;
}

.industry-info h4 {
  margin: 0 0 0.625rem 0; /* 10px -> 0.625rem */
  color: #444;
}

.asset-details p {
  margin: 0.3125rem 0; /* 5px -> 0.3125rem */
  color: #555;
}
</style>
