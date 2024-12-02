<template>
  <div class="community-board">
    <!-- 게시판 제목 -->
    <h1 class="board-title">자유게시판</h1>

    <!-- 버튼 그룹 -->
    <div class="button-group">
      <button v-if="view !== 'list'" @click="changeView('list')">목록 보기</button>
      <button v-if="view === 'list'" @click="changeView('create')">새 글 작성</button>
    </div>

    <!-- 컴포넌트 표시 -->
      <component
        :is="componentMap[view]"
        @goToList="changeView('list')"
        @viewDetail="viewDetail"
        :articleId="selectedArticleId"
      ></component>
    </div>
</template>

<script setup>
import { ref } from "vue";
import ArticleList from "./ArticleList.vue";
import ArticleCreate from "./ArticleCreate.vue";
import ArticleDetail from "./ArticleDetail.vue";

const view = ref("list");
const selectedArticleId = ref(null);

const componentMap = {
  list: ArticleList,
  create: ArticleCreate,
  detail: ArticleDetail,
};

const changeView = (newView) => {
  view.value = newView;
  if (newView !== "detail") {
    selectedArticleId.value = null;
  }
};

const viewDetail = (articleId) => {
  selectedArticleId.value = articleId;
  view.value = "detail";
};
</script>

<style scoped>
/* 전체적인 게시판 레이아웃 스타일 */
.community-board {
  max-width: 90rem; /* 더 넓게 설정 (1440px -> 90rem) */
  margin: 3rem auto; /* 여백 확대 */
  padding: 2.5rem; /* 내부 여백 확장 */
  background-color: #fefefe; /* 거의 흰색 배경 */
  border-radius: 1rem; /* 테두리를 더 부드럽게 */
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.05); /* 은은한 그림자 */
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* 게시판 제목 스타일 */
.board-title {
  text-align: left;
  font-size: 2rem; /* 글씨 크기 확대 */
  font-weight: bolder;
  color: #333333;
  margin-bottom: 2rem; /* 아래 간격을 크게 설정 */
  font-family: 'DoHyeon-Regular', sans-serif;
}

/* 버튼 그룹 스타일 */
.button-group {
  display: flex;
  justify-content: flex-end; /* 버튼을 오른쪽으로 정렬 */
  margin-bottom: 1rem; /* 아래 간격 */
}

button {
  margin-left: 1rem; /* 버튼 간격 */
  padding: 0.5rem 1rem; /* 버튼 크기를 줄임 */
  font-size: 1rem; /* 버튼 글씨 크기 조정 */
  border: 1px solid #ccc; /* 단색 테두리 */
  background-color: transparent; /* 투명 배경 */
  color: #333; /* 버튼 글씨 색상 */
  cursor: pointer;
  border-radius: 0.375rem; /* 부드러운 둥근 테두리 */
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

button:hover {
  background-color: #f5f5f5; /* 호버 시 살짝 밝아짐 */
  border-color: #999; /* 테두리 색상 변경 */
}

/* 컴포넌트 컨테이너 */
.component-container {
  margin-top: 2rem; /* 간격 확대 */
  padding: 1.5rem; /* 내부 여백 */
  border: 0.0625rem solid #e0e0e0; /* 은은한 테두리 */
  border-radius: 0.5rem;
  background-color: #fafafa; /* 연한 배경 */
}
</style>
