<template>
  <div>
    <div class="finance-view">
      <h1>금융 정보</h1>
      <nav class="simple-nav">
        <div class="nav-menu-container">
          <a v-for="(name, key) in menuItems" 
             :key="key"
             @click="changeComponent(key)"
             :class="['nav-link', { active: currentComponent === key }]">
            {{ name }}
          </a>
        </div>
      </nav>

      <div class="content-section">
        <component :is="componentMap[currentComponent]"></component>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useCounterStore } from "@/stores/counter"
import DepositInfo from "@/components/DepositInfo.vue"
import ETFInfo from "@/components/ETFInfo.vue"
import NearbyBanks from "@/components/NearbyBanks.vue"
import ExchangeCalculator from "@/components/ExchangeCalculator.vue"
import CommunityBoard from "@/components/CommunityBoard.vue"

const store = useCounterStore()
const currentComponent = ref("DepositInfo")

// 메뉴 아이템 정의
const menuItems = {
  DepositInfo: '예금정보',
  ETFInfo: 'ETF정보',
  NearbyBanks: '내 주변 은행 찾기',
  ExchangeCalculator: '환율계산기',
  CommunityBoard: '자유게시판'
}

// 컴포넌트 매핑
const componentMap = {
  DepositInfo,
  ETFInfo,
  NearbyBanks,
  ExchangeCalculator,
  CommunityBoard
}

// 컴포넌트 변경 함수
const changeComponent = (componentName) => {
  currentComponent.value = componentName
}

// onMounted 훅에서 getFinances 호출 제거
onMounted(() => {
  // 더 이상 getFinances를 호출하지 않음
})
</script>

<style scoped>
.finance-view {
  max-width: 75rem; /* 1200px -> 75rem */
  margin: 1.25rem auto; /* 20px -> 1.25rem */
  padding: 1.25rem; /* 20px -> 1.25rem */
}

.simple-nav {
  display: flex;
  justify-content: center;
  margin: 1.25rem 0; /* 20px -> 1.25rem */
}

.nav-menu-container {
  display: flex;
  gap: 0.9375rem; /* 15px -> 0.9375rem */
  align-items: center;
}

.nav-link {
  font-family: 'Roboto', sans-serif;
  font-size: 1.5rem; /* 그대로 1.5rem */
  font-weight: 700;
  color: #2c3e50;
  text-decoration: none;
  cursor: pointer;
  padding: 0.3125rem 0.625rem; /* 5px 10px -> 0.3125rem 0.625rem */
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #42b983;
}

.nav-link.active {
  color: #42b983;
  border-bottom: 0.125rem solid #42b983; /* 2px -> 0.125rem */
}

.content-section {
  padding: 1.25rem; /* 20px -> 1.25rem */
  background-color: #f9f9f9;
  border-radius: 0.5rem; /* 8px -> 0.5rem */
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1); /* 2px -> 0.125rem, 4px -> 0.25rem */
  margin-top: 1.25rem; /* 20px -> 1.25rem */
}
</style>
