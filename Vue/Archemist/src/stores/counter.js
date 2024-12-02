import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const finances = ref([]); // 게시글 목록
  const API_URL = "http://127.0.0.1:8000"; // API 기본 URL
  const token = ref(null); // 인증 토큰
  const userProfile = ref(null); // 사용자 프로필
  const isLogin = computed(() => token.value !== null); // 로그인 상태
  const router = useRouter(); // Vue Router

  // 게시글 가져오기
  const getFinances = async function () {
    try {
      const res = await axios({
        method: "get",
        url: `${API_URL}/finances/`,
        headers: {
          Authorization: `Token ${token.value}`, // 인증 헤더 추가
        },
      });
      finances.value = res.data;
    } catch (err) {
      console.error("게시글 가져오기 실패:", err);
    }
  };

  // 회원가입
  const signUp = async function (payload) {
    const { username, password1, password2, email, date_of_birth, avatar } =
      payload;
    try {
      await axios({
        method: "post",
        url: `${API_URL}/accounts/signup/`,
        headers: {
          "Content-Type": "multipart/form-data",
        },
        data: {
          username,
          password1,
          password2,
          email,
          date_of_birth,
          avatar,
        },
      });
      await logIn({ username, password: password1 });
    } catch (err) {
      console.error("회원가입 실패:", err);
    }
  };

  // 로그인
  const logIn = async function (payload) {
    const { username, password } = payload;
    try {
      const res = await axios.post(`${API_URL}/accounts/login/`, {
        username,
        password,
      });
      token.value = res.data.key; // Pinia 상태에 저장
      localStorage.setItem("authToken", res.data.key); // localStorage에 저장

      await fetchUserProfile(); // 프로필 정보 가져오기

      // currentUser를 로컬 스토리지에 저장 (username 저장)
      localStorage.setItem("currentUser", userProfile.value.username);

      router.push({ name: "HomeView" }); // 홈 페이지로 이동
    } catch (err) {
      console.error("로그인 실패:", err);
      alert("로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.");
    }
  };


  // 로그아웃
  const logOut = async function () {
    try {
      await axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
        headers: {
          Authorization: `Token ${token.value}`, // 인증 헤더 추가
        },
      });
      token.value = null;
      userProfile.value = null;
      router.push({ name: "LogInView" }); // 로그인 페이지로 이동
    } catch (err) {
      console.error("로그아웃 실패:", err);
    }
  };

  // 사용자 프로필 정보 가져오기
  const fetchUserProfile = async () => {
    try {
      const response = await axios({
        method: "get",
        url: `${API_URL}/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      userProfile.value = response.data;

      // currentUser 저장
      localStorage.setItem("currentUser", response.data.username);

      return userProfile.value;
    } catch (error) {
      console.error("프로필 가져오기 실패:", error);
      throw error;
    }
  };


  // 사용자 프로필 업데이트
  const updateProfile = async (formData) => {
    try {
      const response = await axios({
        method: "put",
        url: `${API_URL}/accounts/profile/update/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: formData,
      });
      
      // 프로필 업데이트 후 최신 정보 가져오기
      await fetchUserProfile();
      return response.data;
    } catch (error) {
      console.error("프로필 업데이트 실패:", error);
      throw error;
    }
  };


  return {
    finances,
    API_URL,
    getFinances,
    signUp,
    logIn,
    token,
    isLogin,
    logOut,
    userProfile,
    fetchUserProfile,
    updateProfile,
  };
}, { persist: true });
