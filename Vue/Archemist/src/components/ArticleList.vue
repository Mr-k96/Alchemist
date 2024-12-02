<template>
  <div class="article-list">
    <h3></h3>
    <div class="article-container">
      <div 
        v-for="(article, index) in articles" 
        :key="article.id" 
        class="article-item"
        @click="$emit('viewDetail', article.id)"
      >
        <span class="article-index">{{ index + 1 + (currentPage - 1) * pageSize }}</span>
        <div class="article-info">
          <span class="article-title">{{ article.title }}</span>
          <span class="article-meta">
            작성자: {{ article.user }} | 
            작성일: {{ new Date(article.created_at).toLocaleDateString() }} 
            {{ new Date(article.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
          </span>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 버튼 -->
    <div class="pagination">
      <button 
        :disabled="!previousPage" 
        @click="fetchArticles(previousPage)"
      >
        이전
      </button>
      <span>페이지 {{ currentPage }}</span>
      <button 
        :disabled="!nextPage" 
        @click="fetchArticles(nextPage)"
      >
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// API URL 및 데이터 정의
const API_URL = "http://127.0.0.1:8000";
const articles = ref([]); // 현재 페이지 게시글
const currentPage = ref(1); // 현재 페이지 번호
const pageSize = 5; // 페이지당 게시글 수
const nextPage = ref(null); // 다음 페이지 URL
const previousPage = ref(null); // 이전 페이지 URL

// 게시글 데이터 가져오기 함수
const fetchArticles = async (url = `${API_URL}/articles/`) => {
  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Token ${localStorage.getItem("authToken")}`,
      },
    });
    articles.value = response.data.results; // 현재 페이지 데이터
    nextPage.value = response.data.next; // 다음 페이지 URL
    previousPage.value = response.data.previous; // 이전 페이지 URL
    currentPage.value = new URL(url).searchParams.get("page") || 1; // 현재 페이지 번호
  } catch (error) {
    console.error("게시글 목록 가져오기 실패:", error);
    if (error.response?.status === 401) {
      alert("인증이 필요합니다. 다시 로그인하세요.");
    }
  }
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
  fetchArticles();
});
</script>

<style scoped>

h3 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.8rem; /* 28px */
}

.article-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* 항목 간 간격 */
}

.article-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background-color: #f0f7f4; /* 에메랄드 바다색 배경 */
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer; /* 클릭 가능한 영역 표시 */
}

.article-item:hover {
  transform: scale(1.03); /* 살짝 커짐 효과 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* 그림자 강화 */
  background-color: #e6f4f1; /* 호버 시 배경색 변경 */
}

.article-index {
  font-size: 1.1rem;
  font-weight: bold;
  margin-right: 2rem;
  margin-left: 1rem;
}

.article-info {
  flex: 1;
}

.article-title {
  display: block;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  transition: color 0.2s ease; /* 색상 전환 */
}

.article-item:hover .article-title {
  color: #067d68; /* 에메랄드 바다색 강조 */
}

.article-meta {
  font-size: 0.875rem;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 1rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #067d68;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  font-size: 1rem;
  font-weight: bold;
}
</style>
