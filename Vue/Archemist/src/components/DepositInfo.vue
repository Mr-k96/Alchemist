<template>
  <div class="deposit-info">
    <!-- 예금 정보 제목 -->
    <h1>예금정보</h1>

    <!-- 검색 입력창 -->
    <div class="search-section">
      <input v-model="searchTerm" placeholder="상품명 또는 은행명 검색" class="search-input" />
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading">데이터를 불러오는 중입니다...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <!-- 제품 목록 -->
    <div v-if="!loading && !error" class="products-container">
      <div v-for="product in filteredProducts" :key="product.id" class="product-card">
        <div class="product-header">
          <h3>{{ product.fin_prdt_nm }}</h3>
          <span class="bank-name">{{ product.kor_co_nm }}</span>
        </div>
        <div class="interest-rates">
          <h4>금리 정보</h4>
          <table>
            <thead>
              <tr>
                <th>저축 기간</th>
                <th>기본금리</th>
                <th>최고우대금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rate in product.금리정보" :key="rate.id">
                <td>{{ rate.save_trm }}개월</td>
                <td>{{ rate.intr_rate }}%</td>
                <td>{{ rate.intr_rate2 }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref, onMounted, watch } from "vue"
import axios from "axios"

const products = ref([])
const filteredProducts = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref("")

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/deposit/",
  headers: { "Content-Type": "application/json" }
})

const fetchProducts = async () => {
  loading.value = true
  try {
    const response = await api.get("/deposit-products/")
    if (Array.isArray(response.data)) {
      products.value = response.data
    } else if (response.data.data) {
      products.value = response.data.data
    } else {
      products.value = []
    }
    filteredProducts.value = products.value
  } catch (err) {
    error.value = "상품 정보를 불러오는데 실패했습니다."
    console.error("Error details:", err.response?.data || err.message)
  } finally {
    loading.value = false
  }
}

watch(searchTerm, newValue => {
  try {
    if (!products.value) {
      filteredProducts.value = []
      return
    }
    if (!newValue) {
      filteredProducts.value = products.value
      return
    }
    const searchLower = newValue.toLowerCase()
    filteredProducts.value = products.value.filter(product => {
      return (
        product &&
        ((product.fin_prdt_nm && product.fin_prdt_nm.toLowerCase().includes(searchLower)) ||
        (product.kor_co_nm && product.kor_co_nm.toLowerCase().includes(searchLower)))
      )
    })
  } catch (err) {
    console.error("Search error:", err)
    error.value = "검색 중 오류가 발생했습니다."
  }
})

onMounted(fetchProducts)
</script>
  
<style scoped>
/* 전체 컨테이너 */
.deposit-info {
  max-width: 90rem; /* 최대 너비 설정 */
  margin: 3rem auto; /* 중앙 정렬 및 여백 */
  padding: 2rem; /* 내부 여백 */
  background-color: #ffffff; /* 배경색 */
  border-radius: 1rem; /* 둥근 테두리 */
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  font-family: 'Arial', sans-serif; /* 기본 글씨체 */
}

/* 제목 스타일 */
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
}

.products-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(18.75rem, 1fr)); /* 300px -> 18.75rem */
  gap: 1.25rem; /* 20px -> 1.25rem */
}

.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem; /* 8px -> 0.5rem */
  padding: 0.9375rem; /* 15px -> 0.9375rem */
  background-color: white;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1); /* 2px -> 0.125rem, 4px -> 0.25rem */
  transition: transform 0.2s ease, box-shadow 0.2s ease; /* 움직이는 효과와 그림자 효과 */
}

.product-card:hover {
  transform: translateY(-0.125rem); /* 2px 위로 이동 */
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.2); /* 그림자 강도 증가 */
}

.product-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 0.625rem; /* 10px -> 0.625rem */
  margin-bottom: 0.625rem; /* 10px -> 0.625rem */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.625rem; /* 10px -> 0.625rem */
}

th, td {
  padding: 0.5rem; /* 8px -> 0.5rem */
  text-align: center;
  border: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
}

.loading, .error-message {
  text-align: center;
  padding: 1.25rem; /* 20px -> 1.25rem */
  margin: 1.25rem 0; /* 20px -> 1.25rem */
}

.error-message {
  color: red;
  border: 1px solid red;
  border-radius: 0.25rem; /* 4px -> 0.25rem */
}
</style>
