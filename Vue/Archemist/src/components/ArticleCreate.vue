<template>
  <div class="article-create">
    <h2>새 글 작성</h2>
    <form @submit.prevent="createArticle" class="create-form">
      <label for="title">
        제목:
        <input id="title" v-model="title" type="text" required />
      </label>
      <label for="content">
        내용:
        <textarea id="content" v-model="content" required></textarea>
      </label>
      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// 부모 컴포넌트로 이벤트 전달
const emit = defineEmits(["goToList"]);

// Django 서버 URL
const API_URL = "http://127.0.0.1:8000";

// 게시글 제목과 내용
const title = ref("");
const content = ref("");

// 게시글 생성 함수
const createArticle = async () => {
  const tokenValue = localStorage.getItem("authToken"); // 동적으로 토큰 가져오기
  console.log("사용 중인 토큰:", tokenValue); // 디버깅

  if (!tokenValue) {
    alert("로그인이 필요합니다.");
    return;
  }

  try {
    // Axios 요청
    await axios.post(
      `${API_URL}/articles/`,
      {
        title: title.value,
        content: content.value,
      },
      {
        headers: {
          Authorization: `Token ${tokenValue}`, // 인증 토큰 추가
        },
      }
    );
    alert("게시글이 작성되었습니다.");
    emit("goToList"); // 부모 컴포넌트로 이벤트 전달
  } catch (err) {
    console.error("게시글 작성 실패:", err);
    if (err.response?.status === 401) {
      alert("인증 실패: 다시 로그인해주세요.");
    } else {
      alert("게시글 작성 중 오류가 발생했습니다.");
    }
  }
};
</script>

<style scoped>
.create-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0.75rem;
}

label {
  display: flex;
  flex-direction: column;
}

input,
textarea {
  padding: 0.5rem;
  border-radius: 0.25rem;
  border: dotted thin #ddd;
}

textarea {
  height: 12rem; /* 높이를 늘려줍니다 */
  resize: vertical; /* 사용자가 텍스트 영역의 크기를 조절할 수 있도록 설정 */
}

button {
  align-self: flex-end;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #a8dadc;
  color: white;
  border: none;
  border-radius: 0.25rem;
}

button:hover {
  background: #457b9d;
}
</style>
