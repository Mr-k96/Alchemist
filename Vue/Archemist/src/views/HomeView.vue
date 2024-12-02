<template>
  <div class="banner">
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
    <div class="container">
      <h1>Welcome to Alchemist</h1>
      <p class="banner-subtitle">For your beautiful future</p>
      <button v-if="!isLoggedIn" class="login-button" @click="goToLogin">
        Login
      </button>
      <button v-else class="login-button" @click="goToStart">START</button>
    </div>
  </div>
  <div class="article">
    <div class="content">
      <span class="focus">FOCUS</span>
      <span class="issue">ISSUE</span>
    </div>
    <div class="article-container">
      <div class="sector">국내 경제 기사</div>
      <div class="sector-content">
        <div v-for="news in newsList.kr_news" :key="news.id">
          <a :href="news.link" target="_blank">{{ news.title }}</a>
        </div>
      </div>
    </div>
    <div class="article-container">
      <div class="sector">해외 경제 기사</div>
      <div class="sector-content">
        <div v-for="news in newsList.us_news" :key="news.id">
          <a :href="news.link" target="_blank">{{ news.title }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const router = useRouter();
const store = useCounterStore();
const videoPlayer = ref(null);
const newsList = ref({
  kr_news: [],
  us_news: []
});

const videos = [
  new URL("@/asset/Main/Main_video.mp4", import.meta.url).href
];

const currentVideo = ref(videos[0]);

// 로그인 상태 확인
const isLoggedIn = computed(() => store.isLogin);

// 로그인 페이지로 이동
const goToLogin = () => {
  router.push("/login");
};

// START 버튼 클릭 시 새로운 페이지로 이동
const goToStart = () => {
  router.push("/survey");
};

// 뉴스 데이터 가져오기
const fetchNews = async () => {
  try {
    // 절대 경로로 API 엔드포인트 지정
    const response = await axios.get(
      "http://127.0.0.1:8000/news/get-saved-news/"
    );
    newsList.value = response.data.news;
    console.log("뉴스 데이터:", response.data); // 데이터 확인용
  } catch (error) {
    console.error("뉴스 데이터 로딩 실패:", error);
  }
};

// 컴포넌트 마운트 시 뉴스 데이터 가져오기
onMounted(() => {
  if (videoPlayer.value) {
    videoPlayer.value.play();
  }
  fetchNews();
});
</script>

<style scoped>
.banner {
  position: relative;
  display: flex;
  height: 45rem;
  padding: 3.75rem;
  margin-top: 5rem;
  justify-content: center;
  align-items: center;
  gap: 3.75rem;
  align-self: stretch;
  overflow: hidden;
}

.video-background {
  position: absolute;
  top: 5;          /* 상단 정렬 */
  left: 0;         /* 좌측 정렬 */
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  z-index: -1;
  object-fit: cover;
}

.container {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  flex: 1 0 0;
}

h1 {
  color: #fff;
  text-align: center;
  -webkit-text-stroke: 1px rgba(0, 0, 0, 0.05);
  font-family: "Roboto", sans-serif;
  font-size: 5rem;
  font-weight: 700;
  line-height: 1.2;
  /* 라인 높이를 비율로 수정 */
  margin: 0;
}

.banner-subtitle {
  color: #fff;
  text-align: center;
  -webkit-text-stroke: 1px rgba(0, 0, 0, 0.05);
  font-family: "Roboto", sans-serif;
  font-size: 1.5rem;
  font-weight: 400;
  line-height: 1.5;
  margin: 0;
}

.login-button {
  width: 15rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #fff;
  background: transparent;
  color: #fff;
  font-family: "Roboto", sans-serif;
  font-size: 1.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.login-button:active {
  transform: scale(0.98);
}

.article {
  display: flex;
  padding: 5rem 15rem;
  flex-direction: column;
  align-items: flex-start;
  gap: 1.25rem;
  align-self: stretch;
}

.content {
  display: flex;
  height: 5.5rem;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  align-self: stretch;
  border-bottom: 1px solid rgba(0, 0, 0, 0.3);
}

.focus,
.issue {
  font-family: "Roboto", sans-serif;
  font-size: 4rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.2rem;
}

.focus {
  background: linear-gradient(90deg, #122369 0%, #77b8ed 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.issue {
  margin-left: 0.5rem;
  /* 단어 사이 간격 조절 */
  background: linear-gradient(90deg, #d00 0%, #666 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.article-container {
  display: flex;
  padding: 0 0.625rem;
  flex-direction: column;
  align-items: flex-start;
  gap: 1.25rem;
  align-self: stretch;
  border-bottom: 1px solid rgba(0, 0, 0, 0.3);
}

.sector {
  font-family: "Roboto", sans-serif;
  color: #172970;
  font-size: 2.25rem;
  font-style: normal;
  font-weight: 700;
  line-height: 3rem;
  /* 133.333% */
  letter-spacing: -0.1125rem;
}

.sector-content {
  display: flex;
  flex-direction: column;
  padding-left: 0.625rem;
  gap: 0.5rem;
  width: 100%;
}

.sector-content a {
  color: #172970;
  font-family: "Roboto", sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 3rem;
  letter-spacing: -0.075rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.sector-content a:hover {
  color: #0f5b92;
}
</style>
