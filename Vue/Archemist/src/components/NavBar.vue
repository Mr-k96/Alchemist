<template>
  <nav>
    <div class="navbar-content">
      <div class="nav-logo-container">
        <RouterLink :to="{ name: 'HomeView' }" class="nav-logo-text">Alchemist</RouterLink>
      </div>

      <div class="nav-menu-container">
        <!-- 홈 링크 -->
        <RouterLink :to="{ name: 'HomeView' }">Home</RouterLink> |

        <!-- About 링크 -->
        <RouterLink :to="{ name: 'AboutView' }">About</RouterLink> |
        <div class="auth-links">
          <!-- 사용자가 로그인한 경우 -->
          <div v-if="isLoggedIn" class="logged-in-menu">
            <!-- 기사 목록 링크 -->
            <RouterLink :to="{ name: 'FinanceView' }">Finance</RouterLink> |
            <!-- 프로필 링크 -->
            <RouterLink :to="{ name: 'Profile' }">Profile</RouterLink> |
            <!-- 로그아웃 링크. 클릭 시 logOut 함수 호출 -->
            <a href="#" @click.prevent="store.logOut()">Logout</a>
          </div>

          <!-- 사용자가 로그인하지 않은 경우 -->
          <div v-else>
            <!-- 로그인 링크 -->
            <RouterLink :to="{ name: 'LogInView' }">Login</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { computed } from 'vue'

// Pinia 스토어 사용
const store = useCounterStore()
// Vue Router 인스턴스 가져오기
const router = useRouter()

// 로그인 상태를 계산된 속성으로 정의
const isLoggedIn = computed(() => store.isLogin)

</script>

<style scoped>
nav {
  position: sticky;  /* sticky 포지셔닝 적용 */
  top: 0;           /* 상단에 고정 */
  z-index: 1000;    /* 다른 요소들 위에 표시되도록 z-index 설정 */
  background-color: white;  /* 배경색 지정 (스크롤 시 내용이 비치지 않도록) */
  display: inline-flex;
  padding: 1.25rem;
  justify-content: center;
  align-items: center;
  gap: 1.25rem;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  /* 선택적: 그림자 효과 추가 */
}

.navbar-content {
  display: flex;
  max-width: 87.5rem;
  width: 100%;
  padding: 0rem 2.5rem;
  justify-content: space-between;
  align-items: center;
}

.nav-logo-container {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}
.nav-logo-text {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  color: #000 !important;
  font-family: 'Roboto', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 100%;
  text-decoration: none;
}

.nav-logo-text:hover {
  opacity: 0.8;
}

.nav-menu-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: nowrap;
  gap: 0.5rem;
  color: #000;
  font-family: 'Roboto', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5rem;
}

.auth-links {
  display: inline-flex;
  align-items: center;
}

.logged-in-menu {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

nav a {
  font-family: 'Roboto', sans-serif;
  font-weight: 700;
  color: #2c3e50;
  text-decoration: none;
  padding: 0.5rem;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>