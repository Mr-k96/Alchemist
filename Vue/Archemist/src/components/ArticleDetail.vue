<template>
  <div class="article-detail">
    <!-- 제목 -->
    <div class="article-header">
      <h1 
        v-if="!isEditingPost" 
        class="article-title">{{ article?.title || "게시글 제목" }}</h1>
      <input 
        v-else 
        class="article-title-edit" 
        v-model="editTitle" 
        type="text" 
        placeholder="제목을 입력하세요" 
      />

      <div class="action-buttons">
        <button 
          v-if="!isEditingPost && isAuthor" 
          @click="editPost"
        >
          수정
        </button>
        <button 
          v-if="!isEditingPost && isAuthor" 
          @click="confirmDeleteArticle"
        >
          삭제
        </button>
        <button 
          v-if="isEditingPost" 
          @click="updateArticle"
        >
          저장
        </button>
        <button 
          v-if="isEditingPost" 
          @click="cancelEditPost"
        >
          취소
        </button>
      </div>
    </div>

    <!-- 작성자, 작성일, 수정일 -->
    <div class="article-meta">
      <p><strong>작성자:</strong> {{ article?.user || "알 수 없음" }}</p>
      <p><strong>작성일:</strong> {{ new Date(article?.created_at).toLocaleString() || "N/A" }}</p>
      <p><strong>수정일:</strong> {{ new Date(article?.updated_at).toLocaleString() || "N/A" }}</p>
    </div>

    <!-- 내용 -->
    <div 
      class="article-content" 
      :class="{ 'editing': isEditingPost }"
    >
      <textarea 
        v-if="isEditingPost" 
        v-model="editContent" 
        class="content-edit"
      ></textarea>
      <p v-else>{{ article?.content || "내용이 없습니다." }}</p>
    </div>

    <hr />

    <!-- 댓글 -->
    <h3>댓글</h3>
    <ul class="comment-list">
      <li v-if="article?.comments.length === 0">댓글이 없습니다.</li>
      <li 
        v-for="comment in article?.comments" 
        :key="comment.id" 
        class="comment-item"
      >
        <strong>{{ comment.user }}:</strong>
        <div 
          v-if="editingCommentId === comment.id" 
          class="edit-comment-form"
        >
          <textarea v-model="editCommentContent"></textarea>
          <button @click="updateComment(comment.id)">저장</button>
          <button @click="cancelEditComment">취소</button>
        </div>
        <div v-else>
          {{ comment.content }}
          <span>({{ new Date(comment.created_at).toLocaleString() }})</span>
          <button 
            v-if="comment.user === currentUser" 
            @click="editComment(comment)"
          >
            수정
          </button>
          <button 
            v-if="comment.user === currentUser" 
            @click="confirmDeleteComment(comment.id)"
          >
            삭제
          </button>
        </div>
      </li>
    </ul>

    <!-- 댓글 추가 -->
    <form 
      @submit.prevent="addComment" 
      class="add-comment-form"
    >
      <label>
        댓글 작성:
        <textarea v-model="commentContent" required></textarea>
      </label>
      <button type="submit">입력</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";
const article = ref(null); // 게시글 데이터 저장
const commentContent = ref(""); // 댓글 내용 입력
const currentUser = localStorage.getItem("currentUser"); // 현재 로그인한 사용자 username

const props = defineProps({
  articleId: Number, // 부모로부터 전달받은 게시글 ID
});

// defineEmits
const emit = defineEmits(["goToList"]);

const isAuthor = computed(() => article.value?.user === currentUser);

// 게시글 수정 관련 상태
const isEditingPost = ref(false);
const editTitle = ref("");
const editContent = ref("");

// 댓글 수정 관련 상태
const editingCommentId = ref(null);
const editCommentContent = ref("");

const fetchArticleDetail = async () => {
  try {
    const response = await axios.get(`${API_URL}/articles/${props.articleId}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem("authToken")}`,
      },
    });
    article.value = response.data;
  } catch (error) {
    console.error("게시글 상세보기 실패:", error);
    alert("게시글을 불러오는 중 오류가 발생했습니다.");
  }
};

// 게시글 수정
const editPost = () => {
  isEditingPost.value = true;
  editTitle.value = article.value.title;
  editContent.value = article.value.content;
};

const cancelEditPost = () => {
  isEditingPost.value = false;
};

const updateArticle = async () => {
  try {
    const response = await axios.put(
      `${API_URL}/articles/${props.articleId}/`,
      {
        title: editTitle.value,
        content: editContent.value,
      },
      {
        headers: {
          Authorization: `Token ${localStorage.getItem("authToken")}`,
        },
      }
    );
    article.value = response.data;
    isEditingPost.value = false;
    alert("게시글이 수정되었습니다.");
  } catch (error) {
    console.error("게시글 수정 실패:", error);
    alert("게시글 수정 중 오류가 발생했습니다.");
  }
};

// 댓글 수정
const editComment = (comment) => {
  editingCommentId.value = comment.id;
  editCommentContent.value = comment.content;
};

const cancelEditComment = () => {
  editingCommentId.value = null;
};

const updateComment = async (commentId) => {
  try {
    const response = await axios.put(
      `${API_URL}/articles/${props.articleId}/comments/${commentId}/`,
      {
        content: editCommentContent.value,
      },
      {
        headers: {
          Authorization: `Token ${localStorage.getItem("authToken")}`,
        },
      }
    );
    const updatedComment = response.data;
    const index = article.value.comments.findIndex((c) => c.id === commentId);
    article.value.comments[index] = updatedComment;
    editingCommentId.value = null;
    alert("댓글이 수정되었습니다.");
  } catch (error) {
    console.error("댓글 수정 실패:", error);
    alert("댓글 수정 중 오류가 발생했습니다.");
  }
};

// 기존 코드 (게시글 삭제, 댓글 삭제, 댓글 추가)는 유지
const confirmDeleteArticle = () => {
  if (confirm("게시글을 삭제하시겠습니까?")) {
    deleteArticle();
  }
};

const deleteArticle = async () => {
  try {
    await axios.delete(`${API_URL}/articles/${props.articleId}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem("authToken")}`,
      },
    });
    alert("게시글이 삭제되었습니다.");
    emit("goToList");
  } catch (error) {
    console.error("게시글 삭제 실패:", error);
    alert("게시글 삭제 중 오류가 발생했습니다.");
  }
};

const confirmDeleteComment = (commentId) => {
  if (confirm("댓글을 삭제하시겠습니까?")) {
    deleteComment(commentId);
  }
};

const deleteComment = async (commentId) => {
  try {
    await axios.delete(`${API_URL}/articles/${props.articleId}/comments/${commentId}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem("authToken")}`,
      },
    });
    article.value.comments = article.value.comments.filter(
      (comment) => comment.id !== commentId
    );
    alert("댓글이 삭제되었습니다.");
  } catch (error) {
    console.error("댓글 삭제 실패:", error);
    alert("댓글 삭제 중 오류가 발생했습니다.");
  }
};

const addComment = async () => {
  try {
    const response = await axios.post(
      `${API_URL}/articles/${props.articleId}/comments/`,
      { content: commentContent.value },
      {
        headers: {
          Authorization: `Token ${localStorage.getItem("authToken")}`,
        },
      }
    );
    article.value.comments.push(response.data);
    commentContent.value = "";
  } catch (error) {
    console.error("댓글 추가 실패:", error);
    alert("댓글 작성 중 오류가 발생했습니다.");
  }
};

onMounted(() => {
  fetchArticleDetail();
});
</script>

<style scoped>
.article-detail {
  max-width: 80rem;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.article-header {
  position: relative;
}

.article-title {
  font-size: 2.2rem; /* 제목 크기 약간 줄임 */
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: left;
  color: #333;
}

.article-title-edit {
  font-size: 2.2rem; /* 제목 크기 동일하게 유지 */
  font-weight: bold;
  width: 100%;
  border: none; /* 선 제거 */
  border-radius: 0.25rem;
  padding: 0.5rem;
  color: #333;
  background-color: #a8dadc50; /* 에메랄드 색 배경 */
}

.action-buttons {
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  gap: 0.5rem;
}

.action-buttons button {
  background: none;
  border: none;
  color: #007bff;
  font-size: 0.9rem;
  cursor: pointer;
  transition: color 0.2s ease;
}

.action-buttons button:hover {
  color: #0056b3;
  text-decoration: underline;
}

.article-meta {
  margin-bottom: 1.5rem;
  color: #555;
  font-size: 0.9rem;
}

.article-meta p {
  margin: 0.3rem 0;
}

.article-content {
  margin-top: 1rem;
  padding: 1.5rem;
  background-color: #f4f4f4;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  min-height: 200px;
}

.article-content.editing {
  background-color: #a8dadc50; /* 에메랄드 색 */
}

.content-edit {
  width: 100%;
  height: 200px;
  border: none; /* 선 제거 */
  border-radius: 0.25rem;
  padding: 0.5rem;
  font-size: 1rem;
}

.comment-list {
  list-style: none;
  padding: 0;
}

.comment-item {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  background-color: #f1f1f1;
  border-radius: 0.5rem;
}

.comment-item button {
  margin-left: 0.5rem;
  background: none;
  border: none;
  color: #dc3545;
  font-size: 0.9rem;
  cursor: pointer;
  transition: color 0.2s ease;
}

.comment-item button:hover {
  color: #c82333;
  text-decoration: underline;
}

hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 1.5rem 0;
}

.add-comment-form textarea {
  width: 95%; /* 댓글 작성 칸 가로 길이 확장 */
  height: 80px;
  margin-bottom: 10px;
  border-radius: 0.25rem;
  padding: 0.5rem;
  font-size: 1rem;
}

.add-comment-form button {
  margin: 5px 0;
  padding: 5px 15px;
  background: #a8dadc;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: background-color 0.3s ease;
}

.add-comment-form button:hover {
  background-color: #457b9d;
}
</style>
