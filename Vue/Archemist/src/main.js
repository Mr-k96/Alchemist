import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import 'vuetify/styles';

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);


// 카카오맵 API 로드 함수
const loadKakaoMapAPI = () => {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      resolve(); // 이미 로드된 경우
      return;
    }

    const script = document.createElement('script');
    const apiKey = import.meta.env.VITE_KAKAO_MAP_API_KEY; // 환경 변수에서 API 키 가져오기
    console.log("Kakao API Key:", apiKey); // API 키 로그 출력
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&libraries=services&autoload=false`;
    
    script.onload = () => {
      window.kakao.maps.load(() => {
        console.log('카카오맵이 성공적으로 로드되었습니다.');
        resolve();
      });
    };
    
    script.onerror = () => {
      reject(new Error('카카오 맵 스크립트 로드에 실패했습니다.'));
    };
    
    document.head.appendChild(script);
  });
};

// 앱 초기화 및 카카오맵 로드
const initApp = async () => {
  try {
    await loadKakaoMapAPI();
    
    const mapContainer = document.getElementById('map'); // 지도를 표시할 div
    const mapOption = {
      center: new window.kakao.maps.LatLng(37.5665, 126.978), // 서울 중심 좌표
      level: 3, // 확대 레벨
    };

    const map = new window.kakao.maps.Map(mapContainer, mapOption); // 지도 생성
    console.log("Map initialized successfully:", map);
    
  } catch (error) {
    console.error("Error initializing app:", error);
  }
};

// 앱 마운트
initApp().then(() => {
  app.use(pinia);
  app.use(router);
  app.mount('#app');
}).catch(error => {
  console.error("Failed to initialize the application:", error);
});