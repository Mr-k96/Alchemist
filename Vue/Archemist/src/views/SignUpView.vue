<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <div class="avatar-preview">
      <!-- 프로필 이미지 미리보기 -->
      <img v-if="avatarUrl" :src="avatarUrl" alt="Avatar Preview" />
      <!-- 기본 빈 원 (사진이 없는 경우) -->
      <div v-else class="default-avatar"></div>
    </div>
    <form @submit.prevent="signUp">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model.trim="username" required>

      <label for="password1">Password:</label>
      <input type="password" id="password1" v-model.trim="password1" required>

      <label for="password2">Password Confirmation:</label>
      <input type="password" id="password2" v-model.trim="password2" required>

      <label for="email">Email:</label>
      <input type="email" id="email" v-model.trim="email" required>

      <label for="date_of_birth">Date of Birth:</label>
      <input type="date" id="date_of_birth" v-model.trim="dateOfBirth">

      <label for="avatar">Profile Image:</label>
      <input 
        type="file" 
        id="avatar" 
        @change="handleFileUpload"  
        accept="image/*"  
      >

      <input type="submit" value="Sign Up">
    </form>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)
const dateOfBirth = ref(null)
const avatar = ref(null) // 업로드된 파일 상태 저장
const avatarUrl = ref(null) // 이미지 미리보기 URL

const store = useCounterStore()
const router = useRouter()

// 파일 업로드 처리
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    avatar.value = file // 파일 객체 저장
    avatarUrl.value = URL.createObjectURL(file) // 미리보기 URL 생성
  } else {
    avatarUrl.value = null // 파일이 없을 경우 URL 초기화
  }
}

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: email.value,
    date_of_birth: dateOfBirth.value,
    avatar: avatar.value, // 파일 포함
  }
  store.signUp(payload)
}
</script>


<style scoped>
.signup-container {
  max-width: 30rem; /* 400px -> 25rem */
  margin: 3.125rem auto; /* 50px -> 3.125rem */
  padding: 1.25rem; /* 20px -> 1.25rem */
  border-radius: 0.5rem; /* 8px -> 0.5rem */
  box-shadow: 0 0.25rem 0.625rem rgba(0, 0, 0, 0.1); /* 0 4px 10px -> 0 0.25rem 0.625rem */
  background-color: #ffffff;
}

h1 {
  text-align: center;
  margin-bottom: 1.25rem; /* 20px -> 1.25rem */
}

.avatar-preview {
  display: flex;
  justify-content: center;
  margin-bottom: 1.25rem; /* 20px -> 1.25rem */
}

.avatar-preview img {
  width: 6.25rem; /* 100px -> 6.25rem */
  height: 6.25rem; /* 100px -> 6.25rem */
  border-radius: 50%;
  object-fit: cover;
  border: 0.125rem solid rgba(0, 0, 0, 0.2); /* 2px -> 0.125rem */
}

.default-avatar {
  width: 6.25rem; /* 100px -> 6.25rem */
  height: 6.25rem; /* 100px -> 6.25rem */
  border-radius: 50%;
  background-color: #f0f0f0;
  border: 0.125rem solid rgba(0, 0, 0, 0.2); /* 2px -> 0.125rem */
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 0.625rem; /* 10px -> 0.625rem */
}

input[type=text],
input[type=password],
input[type=email],
input[type=date],
input[type=file] {
  padding: 0.625rem; /* 10px -> 0.625rem */
  margin-top: 0.3125rem; /* 5px -> 0.3125rem */
  border-radius: 0.25rem; /* 4px -> 0.25rem */
  border: 0.0625rem solid #ccc; /* 1px -> 0.0625rem */
}

input[type=submit] {
  margin-top: 1.25rem; /* 20px -> 1.25rem */
  padding: 0.625rem; /* 10px -> 0.625rem */
  border-radius: 0.25rem; /* 4px -> 0.25rem */
  border: none;
  background-color: #000000;
  color: white;
}

input[type=submit]:hover {
  background-color: #00000070;
}

/* 반응형 디자인 */
@media (max-width: 48rem) { /* 768px -> 48rem */
  .signup-container {
    max-width: 90%;
    padding: 0.9375rem; /* 15px -> 0.9375rem */
  }

  h1 {
    font-size: 1.5rem; /* 작은 화면에서 제목 크기 조정 */
  }

  .avatar-preview img,
  .default-avatar {
    width: 5rem; /* 80px -> 5rem */
    height: 5rem; /* 80px -> 5rem */
  }

  input[type=text],
  input[type=password],
  input[type=email],
  input[type=date],
  input[type=file] {
    padding: 0.5rem; /* 8px -> 0.5rem */
    font-size: 0.9rem;
  }

  input[type=submit] {
    padding: 0.5rem; /* 8px -> 0.5rem */
    font-size: 1rem;
  }
}
</style>
