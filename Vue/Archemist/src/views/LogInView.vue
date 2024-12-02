<template>
  <div class="background">
    <video
      autoplay
      muted
      loop
      playsinline
      class="video-background"
      ref="videoPlayer"
    >
      <source :src="currentVideo" type="video/mp4" />
    </video>
    <div class="card">
      <div class="form-container">
        <h1>로그인</h1>
        <form @submit.prevent="logIn">
          <input
            class="input"
            type="text"
            id="username"
            placeholder="아이디를 입력하세요"
            v-model.trim="username"
          />
          <input
            class="input"
            type="password"
            id="password"
            placeholder="비밀번호를 입력하세요"
            v-model.trim="password"
          />
          <div class="button-container">
            <input class="login-btn" type="submit" value="로그인" />
            <button class="signup-btn" @click.prevent="goToSignUp">
              회원가입
            </button>
          </div>
        </form>
      </div>
    </div>
    <div class="welcome-text">
      <div>Good for your</div>
      <div>beautiful future</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

const username = ref(null);
const password = ref(null);
const videoPlayer = ref(null);

const store = useCounterStore();
const router = useRouter();

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  };
  store.logIn(payload);
};

const videos = [
  new URL("@/asset/login/login_video1.mp4", import.meta.url).href
];

const currentVideo = ref(videos[0]);

const goToSignUp = () => {
  router.push({ name: "TermsAgreement" });
};

onMounted(() => {
  // 비디오 자동 재생 시작
  if (videoPlayer.value) {
    videoPlayer.value.play();
  }
});
</script>

<style scoped>
/* 기본 레이아웃 */
.background {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 80vh;
  margin-top: 5rem;
  padding: 0 2rem;
  gap: 2rem;
  overflow: hidden;
}

/* 비디오 배경 */
.video-background {
  position: absolute;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: -1;
  object-fit: cover;
}

/* 환영 텍스트 스타일 */
.welcome-text {
  font-family: 'Dancing Script', cursive;
  font-size: 2rem;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  text-align: center;
  line-height: 1.5;
  white-space: nowrap;
  animation: fadeIn 1.5s ease-in;
}

.welcome-text div {
  margin: 10px 0;
}

/* 카드 스타일 */
.card {
  display: flex;
  flex-direction: column;
  width: 28rem;
  min-width: 28rem;
  padding: 3rem;
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* 폼 컨테이너 */
.form-container h1 {
  margin-bottom: 2rem;
  font-size: 2.5rem;
  color: #457b9d;
}

/* 입력 필드 */
.input {
  width: 100%;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border: 0.1rem solid #ddd;
  border-radius: 0.5rem;
  font-size: 1.1rem;
}

.input:focus {
  outline: none;
  border-color: #457b9d;
}

/* 버튼 스타일 */
.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.login-btn,
.signup-btn {
  width: 48%;
  padding: 1rem;
  font-size: 1.1rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.login-btn {
  background: #457b9d;
  color: #fff;
  border: none;
}

.signup-btn {
  background: #fff;
  color: #457b9d;
  border: 0.1rem solid #457b9d;
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .background {
    justify-content: center;
  }
  
  .welcome-text {
    display: none;
  }
  
  .card {
    width: 100%;
    max-width: 28rem;
    min-width: auto;
  }
}

@media (min-width: 768px) {
  .background {
    padding: 0 4rem;
    gap: 3rem;
  }
  
  .welcome-text {
    font-size: 3rem;
  }
}

@media (min-width: 1024px) {
  .background {
    padding: 0 8rem;
    gap: 4rem;
  }
  
  .welcome-text {
    font-size: 4rem;
  }
}

@media (min-width: 1440px) {
  .background {
    padding: 0 25rem;
    gap: 6rem;
  }
}
</style>
