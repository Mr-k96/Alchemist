<template>
  <div class="map-container">
    <h1>내 주변 은행 찾기</h1>

    <!-- 지역 및 검색 버튼 섹션 -->
    <div class="location-filters">
      <div class="filter-group">
        <label for="province">도/시</label>
        <select id="province" v-model="province" @change="updateCities">
          <option value="">선택해주세요</option>
          <option v-for="prov in provinces" :key="prov" :value="prov">{{ prov }}</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="city">시/군/구</label>
        <select id="city" v-model="city">
          <option value="">선택해주세요</option>
          <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="bank">은행</label>
        <select id="bank" v-model="bank">
          <option value="">선택해주세요</option>
          <option v-for="b in banks" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>

      <button @click="searchNearbyBanks" class="btn search-btn">검색</button>
    </div>



    <!-- 카카오맵 출력 -->
    <div id="map" style="width: 100%; height: 400px;"></div>

    <!-- 검색 결과 -->
    <div v-if="nearbyBanks.length" class="results">
      <h3>주변 은행 목록</h3>
      <ul>
        <li
          v-for="(bank, index) in nearbyBanks"
          :key="index"
          @click="moveToMarker(bank)"
        >
          {{ bank.place_name }} - {{ bank.road_address_name || bank.address_name }}
        </li>
      </ul>
    </div>

    <!-- 로딩 및 오류 메시지 -->
    <div v-if="loading" class="loading">데이터를 불러오는 중입니다...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const provinces = ref(["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "대전광역시", "울산광역시", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도", "세종시"]); // 도/시 목록
const cities = ref([]);
const banks = ref(["전체은행", "경남은행", "광주은행", "국민은행", "기업은행", "농협은행", "대구은행", "부산은행", "산업은행", "새마을금고", "수협은행", "신한은행", "신협은행", "씨티은행", "우체국", "우리은행", "전북은행", "제주은행", "중소기업은행", "한국산업은행", "한국스탠다드차타드은행", "KEB하나은행"]); // 은행 목록

const province = ref("");
const city = ref("");
const bank = ref("");
const nearbyBanks = ref([]);
const loading = ref(false);
const error = ref(null);
const markers = ref([]); // 지도 마커 배열
let map = null; // 카카오맵 객체

// 시/군/구 업데이트 함수
const updateCities = () => {
  if (province.value === "서울특별시") {
    cities.value = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"];
  } else if (province.value === "부산광역시") {
    cities.value = ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"];
  } else if (province.value === "대구광역시") {
    cities.value = ["남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구"];
  } else if (province.value === "인천광역시") {
    cities.value = ["강화군", "계양구", "남구", "남동구", "동구", "부평구", "서구", "연수구", "옹진군", "중구"];
  } else if (province.value === "광주광역시") {
    cities.value = ["광산구", "남구", "동구", "북구", "서구"];
  } else if (province.value === "대전광역시") {
    cities.value = ["대덕구", "동구", "서구", "유성구", "중구"];
  } else if (province.value === "울산광역시") {
    cities.value = ["남구", "동구", "북구", "울주군", "중구"];
  } else if (province.value === "경기도") {
    cities.value = ["가평군", "고양시 덕양구", "고양시 일산동구", "고양시 일산서구", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시 소사구", "부천시 오정구", "부천시 원미구", "성남시 분당구", "성남시 수정구", "성남시 중원구", "수원시 권선구", "수원시 영통구", "수원시 장안구", "수원시 팔달구", "시흥시", "안산시 단원구", "안산시 상록구", "안성시", "안양시 동안구", "안양시 만안구", "양주시", "양평군", "여주군", "연천군", "오산시", "용인시 기흥구", "용인시 수지구", "용인시 처인구", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"];
  } else if (province.value === "강원도") {
    cities.value = ["강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"];
  } else if (province.value === "충청북도") {
    cities.value = ["괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "증평군", "진천군", "청원군", "청주시 상당구", "청주시 흥덕구", "충주시"];
  } else if (province.value === "충청남도") {
    cities.value = ["계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "연기군", "예산군", "천안시 동남구", "천안시 서북구", "청양군", "태안군", "홍성군"];
  } else if (province.value === "전라북도") {
    cities.value = ["고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시 덕진구", "전주시 완산구", "정읍시", "진안군"];
  } else if (province.value === "전라남도") {
    cities.value = ["강진군", "고흥군", "곡성군", "광양시", "구례군", "나주시", "담양군", "목포시", "무안군", "보성군", "순천시", "신안군", "여수시", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"];
  } else if (province.value === "경상북도") {
    cities.value = ["경산시", "경주시", "고령군", "구미시", "군위군", "김천시", "문경시", "봉화군", "상주시", "성주군", "안동시", "영덕군", "영양군", "영주시", "영천시", "예천군", "울릉군", "울진군", "의성군", "청도군", "청송군", "칠곡군", "포항시 남구", "포항시 북구"];
  } else if (province.value === "경상남도") {
    cities.value = ["거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "진주시", "창녕군", "창원시 마산합포구", "창원시 마산회원구", "창원시 성산구", "창원시 의창구", "창원시 진해구", "통영시", "하동군", "함안군", "함양군", "합천군"];
  } else if (province.value === "제주도") {
    cities.value = ["서귀포시", "제주시"];
  } else if (province.value === "세종시") {
    cities.value = ["세종시"];



  } else {
    cities.value = [];
  }
};




// 카카오맵 API 동적 로드
const loadKakaoMapAPI = () => {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      resolve(); // 이미 로드된 경우
      return;
    }

    const script = document.createElement("script");
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&libraries=services`;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Kakao Map API"));
    document.head.appendChild(script);
  });
};

// 지도 초기화
const initMap = async () => {
  try {
    await loadKakaoMapAPI();
    
    kakao.maps.load(() => {
      const mapContainer = document.getElementById("map");
      const mapOption = {
        center: new kakao.maps.LatLng(37.5665, 126.978), // 서울 중심 좌표
        level: 3,
      };

      map = new kakao.maps.Map(mapContainer, mapOption);
      console.log("Map initialized successfully:", map);
    });
  } catch (error) {
    console.error("Error initializing map:", error);
  }
};


// 주변 은행 검색
const searchNearbyBanks = () => {
  loading.value = true;
  error.value = null;

  const keyword = `${province.value} ${city.value} ${bank.value !== "전체은행" ? bank.value : ""} 은행`;
  
  console.log("Searching for:", keyword); // 검색 키워드 로그 출력

  const places = new kakao.maps.services.Places();
  places.keywordSearch(keyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      console.log("Search results:", data); // 검색 결과 로그 출력
      displaySearchResults(data);
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
      error.value = "검색 결과가 없습니다.";
    } else {
      error.value = "검색 중 오류가 발생했습니다.";
    }
    loading.value = false;
  });
};

// 검색 결과를 지도와 목록에 표시
const displaySearchResults = (data) => {
  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];

  nearbyBanks.value = data;

  data.forEach((place) => {
    const markerPosition = new kakao.maps.LatLng(place.y, place.x);
    const marker = new kakao.maps.Marker({
      position: markerPosition,
      map: map,
    });

    const infowindow = new kakao.maps.InfoWindow({
      content: `<div style="padding:5px;">${place.place_name}</div>`,
    });

    kakao.maps.event.addListener(marker, "click", () => {
      infowindow.open(map, marker);
    });

    markers.value.push(marker);
  });

  if (data.length > 0) {
    const firstPlace = data[0];
    const centerPosition = new kakao.maps.LatLng(firstPlace.y, firstPlace.x);
    map.setCenter(centerPosition);
  }
};

// 마커 클릭 시 지도 이동
const moveToMarker = (place) => {
  const position = new kakao.maps.LatLng(place.y, place.x);
  map.setCenter(position);
};



onMounted(() => {
  initMap(); // 컴포넌트가 마운트될 때 지도 초기화
});
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.map-container {
  max-width: 80rem; /* 960px -> 60rem */
  margin: 3rem auto; /* 중앙 정렬 */
  padding: 2rem; /* 내부 여백 */
  background-color: #fefefe; /* 흰색 배경 */
  border-radius: 1rem; /* 둥근 테두리 */
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.05); /* 은은한 그림자 */
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* 제목 스타일 */
h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-left: 0.5rem;
  margin-bottom: 2rem;
  margin-top: 0.5rem;
  font-family: 'DoHyeon-Regular', sans-serif;
}

/* 지역 필터 섹션 스타일 */
.location-filters {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filter-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  font-weight: bold;
  font-size: 1rem;
  color: #333;
}

select {
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #ccc;
  font-size: 1rem;
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* 검색 버튼 */
.search-btn {
  background-color: #a8dadc; /* 포인트 색상 */
  color: white;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  align-self: flex-end; /* 버튼 아래 정렬 */
}

.search-btn:hover {
  background-color: #457b9d; /* 포인트 색상 강조 */
  transform: scale(1.05);
}

/* 지도 스타일 */
.map {
  width: 100%;
  height: 20rem; /* 높이를 줄임 */
  border-radius: 1rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1); /* 그림자 */
  margin-bottom: 2rem;
}

/* 결과 섹션 스타일 */
.results {
  margin-top: 2rem;
}

.results h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.results ul {
  list-style: none;
  padding: 0;
}

.results li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
}

.results li:hover {
  background-color: #f1f1f1;
}

/* 로딩 및 오류 메시지 스타일 */
.loading,
.error-message {
  text-align: center;
  font-size: 1.125rem;
  margin-top: 2rem;
  font-family: 'GowunBatang-Regular', sans-serif;
}

.error-message {
  color: #e63946;
  font-weight: bold;
}
</style>