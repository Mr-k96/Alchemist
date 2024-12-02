<template>
  <div class="about-container">
    <!-- Main Content -->
    <main>
      <!-- About Section -->
      <section class="about-section animate-on-scroll from-left">
        <div class="about-content">
          <span class="section-title1">About Us</span>
          <p>'Alchemist'에 방문하신 것을 환영합니다!</p>
          <p>우리 Alchemist는 사용자 맞춤형 <br> 디지털금융 포트폴리오를 제공하는 <br> 혁신적인 온라인 플랫폼입니다.</p>
        </div>
        <div class="about-image">
          <img src="@/asset/AboutUs.png" alt="Senior Couple" />
        </div>
      </section>

      <!-- Team Section -->
      <section class="team-section animate-on-scroll from-right">
        <div class="team-logo">

        </div>
        <span class="team-title">Team Alchemist</span>
        <p>우리는 다양한 데이터와 전문성을 바탕으로 사용자 중심의 혁신적인 솔루션을 개발하고자 있습니다.</p>
        <div class="team-categories">
          <span class="creator">Creators</span>
          <span class="innovator">Innovators</span>
          <span class="dreamer">Dreamers</span>
        </div>
      </section>

      <!-- Vision Section -->
      <section class="vision-section animate-on-scroll from-left">
        <span class="section-title2">Our Vision</span>
        <div class="vision-content">
          <img src="@/asset/Vision.png" alt="Vision Graph" />
          <div class="vision-text">
            <p>우리의 비전은 모든 직장인이 자신의 은퇴를 자신 있게 설계하고, <br> 꿈꾸는 미래를 현실로 만들 수 있는 것입니다.</p>
            <p>'Alchemist'의 혁신적인 서비스로 모두가 자신만의 <br> 맞춤형 디지털금융 포트폴리오를 손쉽게 받아볼 수 있습니다.</p>
          </div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="features-section">
        <div class="feature animate-on-scroll from-right">
          <img src="@/asset/Purpose.png" alt="Purpose" />
          <span class="section-title small">Purpose</span>
          <p>'Alchemist'의 목적은 퇴직연금 상품 선택 과정을 단순화하며, 개인화된 추천을 통해 사용자가 자신의 재정 목표를 달성할 수 있도록 돕는 것입니다.</p>
        </div>
        <div class="feature animate-on-scroll from-left">
          <img src="@/asset/Innovation.png" alt="Innovation" />
          <span class="section-title small">Innovation</span>
          <p>'Alchemist'의 핵심 서비스는 AI 기반의 퇴직연금 포트폴리오 추천 시스템입니다. 사용자의 연령 정보와 위험 선호도를 분석하여, 개인에게 최적화된 퇴직연금 상품 포트폴리오를 제안합니다.
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

const setupScrollAnimations = () => {
  const elements = document.querySelectorAll(".animate-on-scroll");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        } else {
          entry.target.classList.remove("visible");
        }
      });
    },
    { threshold: 0.2 }
  );

  elements.forEach((el) => observer.observe(el));
};

onMounted(() => {
  setupScrollAnimations();
});
</script>

<style scoped>
@font-face {
  font-family: 'GowunBatang-Regular';
  src: url('@/asset/fonts/GowunBatang-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

/* 공통 컨테이너 */
.about-container {
  max-width: 80rem;
  margin: 0 auto;
  padding: 3rem 1.5rem;
  background: linear-gradient(135deg, #d4edda, #cce5ff, #fff3cd);
  /* 연두-하늘-노랑 그라데이션 */
  min-height: 120vh;
}

/* 스크롤 애니메이션 초기 상태 */
.animate-on-scroll {
  opacity: 0;
  transform: translateY(3.125rem);
  transition: all 0.6s ease-out;
}

.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}

.from-left {
  transform: translateX(-3.125rem);
}

.from-right {
  transform: translateX(3.125rem);
}

/* About Section */
.about-section {
  display: flex;
  align-items: center;
  gap: 6rem;
  margin: 6rem 0;
  margin-left: 4rem;
  margin-right: 4rem;
}

.about-content {
  flex: 1;
  font-size: 1.4rem;
  font-weight: 600;
  font-family: 'GowunBatang-Regular', sans-serif;
}

.about-image img {
  width: 100%;
  border-radius: 0.625rem;
  transition: transform 0.3s ease;
}

.about-image img:hover {
  transform: scale(1.1);
}

.about p {
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* Team Section */
.team-section {
  padding: 4rem;
  text-align: center;
  background: #ffffff;
  border-radius: 1rem;
  margin: 5rem 0;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.1);
}

.team-categories span {
  display: inline-block;
  padding: 0.5rem 1.2rem;
  border-radius: 1rem;
  font-size: 1rem;
  margin: 0.5rem;
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* Team Categories 색상 */
.creator {
  background: linear-gradient(45deg, #ff6f61, #ff4081);
  /* 그라데이션 색상 */
  color: white;
}

.innovator {
  background: linear-gradient(45deg, #9b59b6, #8e44ad);
  /* 보라색 그라데이션 */
  color: white;
}

.dreamer {
  background: linear-gradient(45deg, #3498db, #2980b9);
  /* 파란색 그라데이션 */
  color: white;
}

.team-title {
  font-size: 2rem;
  font-weight: bold;
  color: #34495e;
  margin-bottom: 1.5rem;
  display: block;
  text-transform: uppercase;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
  /* 입체 효과 */
}

.team-section p {
  font-family: 'GowunBatang-Regular', sans-serif;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

/* Vision Section */
.vision-section {
  margin: 6rem 0;
}

.vision-title-container {
  display: flex;
  justify-content: flex-end;
  /* 제목을 오른쪽으로 배치 */
  margin-bottom: 2rem;
}

.vision-content {
  display: flex;
  gap: 12rem;
  align-items: center;
}

.vision-content img {
  margin-top: 2rem;
  width: 25%;
  transform: translateX(6rem);
  transition: transform 0.3s ease, width 0.3s ease;
}

.vision-content img:hover {
  transform: translateX(7rem) scale(1.1);
}

.vision-text {
  flex: 1;
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* Features Section */
.features-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3rem;
  margin: 6rem 0;
}

.feature {
  padding: 3rem;
  border-radius: 1rem;
  background-color: #ffffff;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.1);
  text-align: center;
}

.feature img {
  width: 80px;
  margin: 0 auto 1rem;
  display: block;
}

/* Features Section */
.feature p {
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* 제목 스타일 */
.section-title1 {
  font-size: 3rem;
  /* 제목 크기 조정 */
  font-weight: bold;
  color: #34495e;
  margin-bottom: 1.5rem;
  display: block;
  text-transform: uppercase;
  font-family: 'Roboto', sans-serif;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
  /* 텍스트에 그림자 효과로 입체감 추가 */
}

.section-title2 {
  font-size: 3rem;
  /* 제목 크기 조정 */
  font-weight: bold;
  color: #34495e;
  margin-left: 5rem;
  margin-bottom: 1.5rem;
  display: block;
  text-transform: uppercase;
  font-family: 'Roboto', sans-serif;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
  /* 텍스트에 그림자 효과로 입체감 추가 */
}

/* 소제목 스타일 */
.section-title.small {
  font-size: 2rem;
  /* 소제목 크기 */
  font-weight: bold;
  padding-bottom: 1rem;
  background: linear-gradient(45deg, #1abc9c, #16a085);
  /* 다른 그라데이션 색상 */
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 1.5rem;
  /* 소제목 아래 간격 추가 */
}

/* 소제목 스타일 */
.section-title.small {
  font-size: 2rem;
  /* 소제목 크기 */
  font-weight: bold;
  padding-bottom: 1rem;
  background: linear-gradient(45deg, #1abc9c, #16a085);
  /* 다른 그라데이션 색상 */
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;

  /* 소제목 스타일 */
  .section-title.small {
    font-size: 2rem;
    /* 소제목 크기 */
    font-weight: bold;
    padding-bottom: 1rem;
    background: linear-gradient(45deg, #1abc9c, #16a085);
    /* 다른 그라데이션 색상 */
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;

    /* 소제목 스타일 */
    .section-title.small {
      font-size: 2rem;
      /* 소제목 크기 */
      font-weight: bold;
      padding-bottom: 1rem;
      background: linear-gradient(45deg, #1abc9c, #16a085);
      /* 다른 그라데이션 색상 */
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      margin-bottom: 1.5rem;
      /* 소제목 아래 간격 추가 */
    }

    /* 본문 텍스트 스타일 */
    .feature p {
      font-size: 1.2rem;
      font-weight: 600;
      font-family: 'GowunBatang-Regular', sans-serif;
      margin-top: 1rem;
      /* 본문과 소제목 사이 간격 추가 */
    }

  }

  /* 본문 텍스트 스타일 */
  .feature p {
    font-size: 1.2rem;
    font-weight: 600;
    font-family: 'GowunBatang-Regular', sans-serif;
    margin-top: 1rem;
    /* 본문과 소제목 사이 간격 추가 */
  }

}

/* 본문 텍스트 스타일 */
.feature p {
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'GowunBatang-Regular', sans-serif;
  margin-top: 1rem;
  /* 본문과 소제목 사이 간격 추가 */
}



/* Team Categories 색상 */
.creator {
  background: linear-gradient(45deg, #ff6f61, #ff4080);
  /* 그라데이션 색상 */
  color: white;
}

.innovator {
  background: linear-gradient(45deg, #59b6a2, #44ada4);
  /* 보라색 그라데이션 */
  color: white;
}

.dreamer {
  background: linear-gradient(45deg, #3498db, #2980b9);
  /* 파란색 그라데이션 */
  color: white;
}

/* Team Section */
.team-title {
  font-size: 2rem;
  font-weight: bold;
  color: #34495e;
  margin-bottom: 1.5rem;
  display: block;
  text-transform: uppercase;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
  /* 입체 효과 */
}

/* Vision Section */
.vision-content img {
  margin-top: 2rem;
  width: 25%;
  transform: translateX(6rem);
  transition: transform 0.3s ease, width 0.3s ease;
}

.vision-content img:hover {
  transform: translateX(7rem) scale(1.1);
}

.vision-text {
  flex: 1;
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* Features Section */
.features-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3rem;
  margin: 6rem 0;
}

.feature {
  padding: 3rem;
  border-radius: 1rem;
  background-color: #ffffff;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.1);
  text-align: center;
}

.feature img {
  width: 80px;
  margin: 0 auto 1rem;
  display: block;
}

.feature p {
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'GowunBatang-Regular', sans-serif;
}

/* 반응형 */
@media (max-width: 48rem) {

  .about-section,
  .vision-content {
    flex-direction: column;
  }

  .features-section {
    grid-template-columns: 1fr;
  }

  /* 제목과 소제목 스타일 */
  .section-title1 {
    font-size: 2.5rem;
    /* 화면 작을 때 제목 크기 조정 */
  }

  .section-title2 {
    font-size: 2.5rem;
    /* 화면 작을 때 제목 크기 조정 */
  }

  .section-title.small {
    font-size: 1.8rem;
    /* 화면 작을 때 소제목 크기 조정 */
  }
}
</style>
