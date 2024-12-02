<template>
  <div class="profile-container">
    <div class="profile-card">
      <!-- 제목 -->
      <h1 class="profile-title">{{ `${store.userProfile.username}'s Profile` }}</h1>

      <!-- 프로필 아바타 -->
      <div class="profile-avatar">
        <img v-if="avatarPreview || store.userProfile.avatar"
          :src="avatarPreview || getAvatarUrl(store.userProfile.avatar)" alt="프로필 이미지" />
        <div v-else class="default-avatar">
          <span>{{ store.userProfile.username.charAt(0).toUpperCase() }}</span>
        </div>
      </div>

      <!-- 프로필 정보 -->
      <div class="profile-info">
        <div class="info-item">
          <strong>이름:</strong>
          <p>{{ store.userProfile.username }}</p>
        </div>
        <div class="info-item">
          <strong>이메일:</strong>
          <p v-if="!isEditing">{{ store.userProfile.email }}</p>
          <input v-else v-model="editedProfile.email" type="email" required />
        </div>
        <div class="info-item">
          <strong>생년월일:</strong>
          <p v-if="!isEditing">{{ formatDate(store.userProfile.date_of_birth) }}</p>
          <input v-else v-model="editedProfile.date_of_birth" type="date" required />
        </div>
        <!-- 프로필 정보의 이미지 부분만 교체 -->
        <div class="info-item">
          <strong>프로필 이미지:</strong>
          <div v-if="!isEditing">
            <p class="file-name">{{ getImageFileName(store.userProfile.avatar) || "이미지 없음" }}</p>
          </div>
          <div v-else>
            <input type="file" @change="handleFileUpload" accept="image/*" class="file-input" />
            <p v-if="editedProfile.avatar" class="file-name">
              선택된 파일: {{ editedProfile.avatar.name }}
            </p>
          </div>
        </div>
      </div>

      <!-- 저장/취소 버튼 -->
      <div class="action-buttons" v-if="isEditing">
        <button class="save-button" @click.prevent="updateProfile">저장</button>
        <button class="cancel-button" @click.prevent="cancelEditing">취소</button>
      </div>
      <button v-else class="edit-button" @click="startEditing">수정하기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const isEditing = ref(false);
const editedProfile = reactive({});
const avatarPreview = ref(null);

const fetchProfile = async () => {
  try {
    await store.fetchUserProfile();
    Object.assign(editedProfile, store.userProfile);
  } catch (error) {
    console.error("프로필 로딩 실패:", error);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "미설정";
  return new Date(dateString).toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const getAvatarUrl = (avatarPath) => {
  if (!avatarPath) return null;

  if (avatarPath.startsWith('http')) {
    return avatarPath;
  }

  return `${store.API_URL}${avatarPath}`;
};

const getImageFileName = (avatarPath) => {
  if (!avatarPath) return "";
  return avatarPath.split('/').pop();
};

const startEditing = () => {
  isEditing.value = true;
  Object.assign(editedProfile, store.userProfile);
};

const cancelEditing = () => {
  isEditing.value = false;
  avatarPreview.value = null;
  Object.assign(editedProfile, store.userProfile);
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    editedProfile.avatar = file; // 파일 객체 저장
    avatarPreview.value = URL.createObjectURL(file); // 미리보기 URL 생성
  }
};

const updateProfile = async () => {
  try {
    const formData = new FormData();
    formData.append("email", editedProfile.email);
    formData.append("date_of_birth", editedProfile.date_of_birth);
    if (editedProfile.avatar instanceof File) {
      formData.append("avatar", editedProfile.avatar); // 새로운 이미지가 있다면 추가
    }

    const response = await store.updateProfile(formData);
    console.log("프로필 업데이트 성공:", response);
    isEditing.value = false;
    avatarPreview.value = null;
    await fetchProfile(); // 최신 프로필 정보 불러오기
  } catch (error) {
    console.error("프로필 업데이트 실패:", error.response?.data || error.message);
  }
};

onMounted(() => {
  fetchProfile();
});
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #d4f3f0, #bfe3e0, #a8dadc);
  /* 부드러운 파스텔톤 청록 그라데이션 */
}

/* 프로필 카드 */
.profile-card {
  width: 100%;
  max-width: 600px;
  background: #ffffff;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  text-align: center;
  animation: fadeIn 0.8s ease-in-out;
  /* 카드 부드럽게 나타나는 효과 */
}

/* 제목 */
.profile-title {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-family: 'Roboto', sans-serif;
}

/* 아바타 */
.profile-avatar {
  width: 200px;
  height: 200px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 5px solid #a8dadc;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  background: #f9f9f9;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #d4f3f0;
  /* 아바타 배경색 */
  color: #457b9d;
  font-size: 2rem;
}

/* 정보 스타일 */
.profile-info {
  margin-top: 1.5rem;
  text-align: left;
}

.info-item {
  margin-bottom: 1.5rem;
}

.info-item p {
  font-size: 1.1rem;
  color: #4d6466;
}

/* 버튼 스타일 */
.action-buttons button,
.edit-button {
  width: 100%;
  max-width: 150px;
  margin: 0.5rem;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  border: none;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.save-button {
  background-color: #57c1b6;
  /* 파스텔톤 청록 */
}

.cancel-button {
  background-color: #ff6b6b;
  /* 부드러운 빨강 */
}

.edit-button {
  background-color: #88dad7;
  /* 밝은 청록 */
}

.save-button:hover {
  background-color: #3fa49d;
}

.cancel-button:hover {
  background-color: #e63946;
}

.edit-button:hover {
  background-color: #6bc8c5;
}

.file-name {
  margin-top: 0.5rem;
  font-size: 1rem;
  color: #4d6466;
  font-style: italic;
}

.file-input {
  margin: 0.5rem 0;
  padding: 0.5rem;
  width: 100%;
  max-width: 300px;
}

/* 애니메이션 효과 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
