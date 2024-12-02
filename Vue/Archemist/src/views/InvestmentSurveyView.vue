<template>
    <div class="investment-survey">
        <form @submit.prevent="submitSurvey">
            <h1>투자 성향 측정</h1>
            <div v-for="(question, index) in questions" :key="index" class="question">
                <h3>{{ question.text }}</h3>
                <div v-for="(choice, choiceIndex) in question.choices" :key="choiceIndex" class="choice">
                    <div class="choice-container">
                        <input type="radio" :id="`q${index}c${choiceIndex}`" :name="`question${index}`"
                            :value="choiceIndex" v-model="answers[index]">
                        <label :for="`q${index}c${choiceIndex}`">{{ choice }}</label>
                    </div>
                </div>
            </div>
            <div class="button-container">
                <button type="submit" :disabled="!isAllAnswered">제출하기</button>
            </div>
        </form>
        <div>
            <!-- 팝업창 -->
            <div v-if="showPopup" class="popup">
                <div class="popup-content">
                    <span class="close" @click="closePopup">&times;</span>

                    <!-- 투자 성향 결과에 따른 이미지 표시 -->
                    <img :src="resultImage" alt="투자 성향 이미지" class="result-image" />
                    <!-- '다음으로' 버튼 표시-->
                    <button v-if="showPopup" class="next-button-outside" @click="goToNextPage">다음으로</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useSurveyStore } from '@/stores/survey';

const router = useRouter()
const store = useSurveyStore()

const questions = ref([
    {
        text: "1. 고객님의 금융상품에 대한 이해 수준은 어느 정도라고 생각하십니까?",
        choices: [
            "파생 상품을 포함한 대부분의 금융투자상품의 구조 및 위험을 상품설명서 등을 읽고 스스로 이해할 수 있음", // 4점
            "널리 알려진 금융투자상품(주식, 채권, 펀드 등)의 구조 및 위험을 이해하고 있음", // 3점
            "널리 알려진 금융투자상품(주식, 채권, 펀드 등)의 특징을 일정 부분 이해하고 있으며 설명을 들으면 구조와 위험을 이해할 수 있음", // 2점
            "금융투자상품에 대해 스스로 결정을 해 본 적이 없음" // 1점
        ]
    },
    {
        text: "2. 고객님께서 투자하신 경험이 있는 금융자산 또는 투자형태는 어떤 것입니까?",
        choices: [
            "원금 보존", // 1점
            "안정적인 수익", // 2점
            "높은 수익", // 3점
            "매우 높은 수익" // 4점
        ]
    },
    {
        text: "3. 고객님의 총 금융자산 규모는 다음 중 어느 수준이십니까?",
        choices: [
            "10억 원 이상", // 1점
            "5억 원 이상 ~ 10억 원 미만", // 2점
            "1억 원 이상 ~ 5억 원 미만", // 3점
            "5천만 원 이상 ~ 1억 원 미만" // 4점
        ]
    },
    {
        text: "4. 고객님의 총 금융자산대비 금융투자상품(주식, 펀드, 채권, 파생상품 등)은 어느 정도의 비중을 차지합니까?",
        choices: [
            "70% 이상", // 5점
            "50% 이상 ~ 70% 미만", // 4점
            "30% 이상 ~ 50% 미만", // 3점
            "10% 이상 ~ 30% 미만", // 2점
            "10% 미만" // 1점
        ]
    },
    {
        text: "5. 고객님께서 투자한 금융투자상품(주식, 펀드, 채권, 파생상품 등)의 투자경험기간은 총 얼마나 되십니까?",
        choices: [
            "10년 이상", // 5점
            "5년 이상 ~ 10년 미만", // 4점
            "3년 이상 ~ 5년 미만", // 3점
            "1년 이상 ~ 3년 미만", // 2점
            "1년 미만" // 1점
        ]
    },
    {
        text: "6. 고객님과 고객님의 가족을 포함하여 현재와 미래의 소득수준을 가장 잘 표현한 것은 어느 것입니까?",
        choices: [
            "현재 안정적인 소득수준이 유지 혹은 증가 예상", // 5점
            "현재 소득수준이 감소 예상", // 4점
            "현재 소득수준이 불안정하며 미래에 소득수준 감소 예상", // 3점
            "현재 소득수준이 불안정하며 미래에 큰 폭으로 악화될 것으로 예상" // 2점
        ]
    },
    {
        text: "7. 고객님께서 금융상품 투자를 통해 기대하는 수익과 감수할 수 있는 손실을 가장 잘 표현한 것은 어느 것입니까?",
        choices: [
            "원금 초과 손실까지 감수하며 적극적인 투자를 통하여 시장수익률(예: 주가지수)을 초과하는 높은 수익을 추구", // 5점
            "원금손실을 감수하며 시장수익률과 비슷한 수준의 수익을 기대", // 4점
            "원금의 일부 손실을 감수하며 시중금리보다 다소 높은 수준의 수익을 기대", // 3점
            "제한적인 손실을 감수하며 시중금리 수준의 수익을 기대" // 2점
        ]
    },
    {
        text: "8. 고객님께서 통상적으로 투자하고자 하는 자금의 투자예상 기간은 얼마나 되십니까?",
        choices: [
            "3년 이상", // 5점
            "1년 이상 ~ 3년 미만", // 3점
            "1년 미만" // 1점
        ]
    }
])

const answers = ref(new Array(questions.value.length).fill(null)) // 각 질문에 대해 빈 배열로 초기화

const isAllAnswered = computed(() => {
    return answers.value.every(answer => answer !== null)
})

const showPopup = ref(false) // 팝업 표시 상태 관리
const totalScore = ref(0) // 총 점수 저장 변수
const resultImage = ref('') // 투자 성향 결과에 따른 이미지 경로
const investmentType = ref('') // 투자 성향 저장 변수

// 점수를 계산하는 함수
const calculateScore = () => {
    const scores = [
        [4, 3, 2, 1], // 첫 번째 질문
        [1, 2, 3, 4], // 두 번째 질문
        [1, 2, 3, 4], // 세 번째 질문
        [5, 4, 3, 2, 1], // 네 번째 질문
        [5, 4, 3, 2, 1], // 다섯 번째 질문
        [5, 4, 3, 2], // 여섯 번째 질문
        [5, 4, 3, 2], // 일곱 번째 질문
        [5, 3, 1] // 여덟 번째 질문
    ];

    return answers.value.reduce((accumulator, answerIndex, questionIndex) => {
        if (answerIndex !== null) {
            return accumulator + scores[questionIndex][answerIndex];
        }
        return accumulator;
    }, 0);
};

// 투자 성향 결정 함수
const determineInvestmentType = (score) => {
    if (score <= 10) return '안정형';
    else if (score <= 15) return '안정추구형';
    else if (score <= 20) return '위험중립형';
    else if (score <= 25) return '적극투자형';
    else return '공격투자형';
};

// 투자 성향에 따른 이미지 경로 설정 함수
const setResultImage = (type) => {
    switch (type) {
        case '안정형':
            resultImage.value = '/survey_result_1.png'; // 안정형 이미지 경로
            break;
        case '안정추구형':
            resultImage.value = '/survey_result_2.png'; // 안정추구형 이미지 경로
            break;
        case '위험중립형':
            resultImage.value = '/survey_result_3.png'; // 위험중립형 이미지 경로
            break;
        case '적극투자형':
            resultImage.value = '/survey_result_4.png'; // 적극투자형 이미지 경로
            break;
        case '공격투자형':
            resultImage.value = '/survey_result_5.png'; // 공격투자형 이미지 경로
            break;
    }
};
const submitSurvey = () => {
    if (isAllAnswered.value) {
        totalScore.value = calculateScore();
        investmentType.value = determineInvestmentType(totalScore.value);

        store.setInvestmentType(investmentType)

        setResultImage(investmentType.value); // 결과 이미지 설정
        showPopup.value = true; // 팝업 표시

        console.log('Survey answers:', answers.value);
        console.log('Total Score:', totalScore.value);
        console.log('Investment Type:', investmentType.value);
    }
};

// 팝업 닫기 함수
const closePopup = () => {
    showPopup.value = false;
};

// 다음 페이지로 이동하는 함수
const goToNextPage = () => {
    router.push({ name: 'PreferAsset' });
};
</script>

<style scoped>
.investment-survey {
    max-width: 75rem;
    margin: 0 auto; 
    margin-top: 6rem;
    margin-bottom: 6rem;
    display: flex;
    justify-content: center;
    align-items: center;
}

h1 {
    padding-bottom: 3rem;
}

h3 {
    padding-bottom: 1rem;
}

.question {
    margin-bottom: 3.75rem;
}

.choice-container {
    display: flex;
    align-items: center;
    gap: 0.9375rem;
    margin-bottom: 0.625rem;
    margin-left: 1rem;
}

.button-container {
    display: flex;
    justify-content: center;
    padding-top: 3.75rem;
}

button {
    padding: 0.9375rem 4.375rem;
    font-size: 1em;
    background-color: #000000;
    color: white;
    border: none;
    border-radius: 0.625rem;
}

button:disabled {
    background-color: #cccccc;
}

button:hover {
    background: rgba(0, 0, 0, 0.75);
}

/* 팝업 스타일 */
.popup {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.popup-content {
    background: white;
    padding: 1.25rem;
    border-radius: 0.3125rem;
}

.result-image {
    max-width: 100%;
    height: auto;
}

.close {
    cursor: pointer;
}

/* 팝업 스타일 */
.popup {
    position: fixed;
    /* 화면 중앙 고정 */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    /* 반투명 배경 */
    display: flex;
    justify-content: center;
    align-items: center;
}

.popup-content {
    position: relative;  /* 자식 요소의 기준점 */
    background: white;
    padding: 0;
    border-radius: 3.125rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 90%;
    margin: 1.25rem;
}

/* 결과 이미지 스타일 */
.result-image {
    width: 100%;
    height: auto;
    display: block;
}

/* 닫기 버튼 스타일 */
.close {
    position: absolute;
    top: 1.25rem;
    right: 1.875rem;
    font-size: 1.875rem;
    font-weight: bold;
    cursor: pointer;
}

/* '다음으로' 버튼 스타일 */
.next-button-outside {
    position: absolute;  /* 팝업 컨텐츠 기준으로 위치 설정 */
    bottom: 3rem;       /* 하단에서의 거리 */
    left: 50%;          /* 가운데 정렬을 위한 설정 */
    transform: translateX(-50%);  /* 정확한 가운데 정렬 */
    padding: 0.9375rem 4.375rem;
    font-size: 1em;
    background-color: #000000;
    color: white;
    border: none;
    border-radius: 0.625rem;
    z-index: 2;         /* 이미지 위에 표시되도록 설정 */
}

.next-button-outside:hover {
    background: rgba(0, 0, 0, 0.75);
}
</style>