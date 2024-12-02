<template>
    <div class="terms-agreement">
        <h1>약관 동의</h1>
        <div class="checkbox-group">
            <label>
                <input type="checkbox" v-model="allAgreed" @change="toggleAll">
                전체 동의하기
            </label>
        </div>
        <div class="additional-info">
            실명 인증된 아이디로 가입, 위치기반서비스 이용약관(선택), 이벤트・혜택 정보 수신(선택) 동의를 포함합니다.
        </div>
        <div class="checkbox-group" v-for="(term, index) in terms" :key="index">
            <label>
                <input type="checkbox" v-model="term.agreed" @change="updateAgreement">
                {{ term.title }}
            </label>
            <div class="terms-content" v-html="formatContent(term.content)"></div>
        </div>
        <div class="button-container">
            <button :disabled="!isAllAgreed" @click="proceedToSignup">동의합니다</button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const terms = ref([
    {
        title: '이용약관', content: `제1조 (목적)
    
  본 약관은 Archemist(이하 "회사")가 제공하는 서비스의 이용과 관련하여 회사와 이용자 간의 권리, 의무 및 책임사항을 규정함을 목적으로 합니다.
    
  제2조 (정의)
    
  1. "서비스"란 회사가 제공하는 모든 서비스를 의미합니다.
  2. "이용자"란 본 약관에 따라 회사가 제공하는 서비스를 이용하는 회원 및 비회원을 말합니다.
  3. "회원"이란 회사에 개인정보를 제공하여 회원등록을 한 자로서, 회사의 정보를 지속적으로 제공받으며 서비스를 이용할 수 있는 자를 말합니다.
    
  제3조 (약관의 효력 및 변경)
    
  1. 본 약관은 서비스를 이용하고자 하는 모든 이용자에 대하여 그 효력을 발생합니다.
  2. 회사는 약관의 규제에 관한 법률 등 관련법을 위배하지 않는 범위에서 본 약관을 변경할 수 있습니다.
  3. 회사가 약관을 변경할 경우에는 적용일자 및 개정사유를 명시하여 현행약관과 함께 서비스 초기화면에 그 적용일자 7일 이전부터 공지합니다.
    
  제4조 (이용자의 의무)
    
  1. 이용자는 다음 행위를 하여서는 안됩니다:
     - 회원가입 신청 시 허위내용을 등록하는 행위
     - 타인의 정보를 도용하는 행위
     - 회사가 게시한 정보를 변경하는 행위
     - 회사의 서비스를 이용하여 법령 또는 이 약관이 금지하는 행위를 하는 경우
    
  제5조 (서비스의 제공 및 중단)
    
  1. 회사는 컴퓨터 등 정보통신설비의 보수점검, 교체 및 고장, 통신의 두절 등의 사유가 발생한 경우에는 서비스의 제공을 일시적으로 중단할 수 있습니다.
  2. 제1항에 의한 서비스 중단의 경우에는 회사는 제8조에 정한 방법으로 이용자에게 통지합니다.
    
  제6조 (개인정보보호)
    
  1. 회사는 이용자의 개인정보 수집 시 서비스제공을 위하여 필요한 범위에서 최소한의 개인정보를 수집합니다.
  2. 회사는 회원가입시 구매계약이행에 필요한 정보를 미리 수집하지 않습니다.
    
  제7조 (저작권의 귀속 및 이용제한)
    
  1. 회사가 작성한 저작물에 대한 저작권 기타 지적재산권은 회사에 귀속됩니다.
  2. 이용자는 서비스를 이용함으로써 얻은 정보를 회사의 사전 승낙 없이 복제, 송신, 출판, 배포, 방송 기타 방법에 의하여 영리목적으로 이용하거나 제3자에게 이용하게 하여서는 안됩니다.
    
  제8조 (분쟁해결)
    
  1. 회사는 이용자가 제기하는 정당한 의견이나 불만을 반영하고 그 피해를 보상처리하기 위하여 고객서비스센터를 설치·운영합니다.
  2. 회사와 이용자 간에 발생한 분쟁은 전자거래기본법, 전자거래소비자보호법, 전자상거래 등에서의 소비자보호에 관한 법률 등 관련법령의 규정에 따라 처리합니다.
    
  제9조 (면책조항)
    
  회사는 천재지변 또는 이에 준하는 불가항력으로 인하여 서비스를 제공할 수 없는 경우에는 서비스 제공에 관한 책임이 면제됩니다.
    
  제10조 (관할법원)
    
  본 약관과 관련된 소송의 관할법원은 민사소송법상의 관할법원으로 합니다.
    
  부칙
  본 약관은 2024년 11월 9일부터 시행합니다.`,
        agreed: false
    },
    {
        title: '개인정보 수집 및 이용', content: `개인정보 수집 및 이용 동의서
    
Archemist(이하 '회사')는 개인정보보호법에 따라 이용자의 개인정보 보호 및 권익을 보호하고 개인정보와 관련한 이용자의 고충을 원활하게 처리할 수 있도록 다음과 같은 처리방침을 두고 있습니다.
    
회사는 개인정보처리방침을 개정하는 경우 웹사이트 공지사항(또는 개별공지)을 통하여 공지할 것입니다.
    
1. 개인정보의 처리 목적
회사는 개인정보를 다음의 목적을 위해 처리합니다. 처리한 개인정보는 다음의 목적 이외의 용도로는 사용되지 않으며 이용 목적이 변경될 시에는 사전동의를 구할 예정입니다.
    
회사는 서비스 제공을 위해 필요한 최소한의 개인정보를 수집하고 있습니다. 수집하는 개인정보 항목은 이메일 주소(아이디), 비밀번호, 이름, 휴대전화번호를 필수항목으로 수집하고 있으며, 프로필 이미지, 소속 기관/회사, 직무는 선택항목으로 수집하고 있습니다. 또한 서비스 이용 과정에서 IP 주소, 쿠키, 서비스 이용 기록, 기기정보가 자동으로 생성되어 수집될 수 있습니다.
    
2. 개인정보의 처리 및 보유 기간
회사는 법령에 따른 개인정보 보유·이용기간 또는 정보주체로부터 개인정보를 수집 시에 동의 받은 개인정보 보유·이용기간 내에서 개인정보를 처리·보유합니다. 회원 탈퇴 시 개인정보는 즉시 파기됩니다. 단, 관계법령의 규정에 의하여 보존할 필요가 있는 경우 회사는 아래와 같이 관계법령에서 정한 일정한 기간 동안 회원정보를 보관합니다.
    
- 계약 또는 청약철회 등에 관한 기록: 5년
- 대금결제 및 재화 등의 공급에 관한 기록: 5년
- 소비자의 불만 또는 분쟁처리에 관한 기록: 3년
- 로그인 기록: 3개월
    
3. 개인정보의 제3자 제공
회사는 정보주체의 동의, 법률의 특별한 규정 등 개인정보 보호법 제17조 및 제18조에 해당하는 경우에만 개인정보를 제3자에게 제공합니다. 현재 회사는 이용자의 개인정보를 제3자에게 제공하고 있지 않습니다.
    
4. 정보주체의 권리, 의무 및 그 행사방법
이용자는 개인정보주체로서 다음과 같은 권리를 행사할 수 있습니다.
- 개인정보 열람요구
- 오류 등이 있을 경우 정정 요구
- 삭제요구
- 처리정지 요구
    
5. 개인정보의 파기
회사는 원칙적으로 개인정보 처리목적이 달성된 경우에는 지체없이 해당 개인정보를 파기합니다. 파기의 절차, 기한 및 방법은 다음과 같습니다.
    
파기절차: 이용자가 입력한 정보는 목적 달성 후 별도의 DB에 옮겨져 내부 방침 및 기타 관련 법령에 따라 일정기간 저장된 후 혹은 즉시 파기됩니다.
    
파기방법: 전자적 파일 형태의 정보는 기록을 재생할 수 없는 기술적 방법을 사용하여 삭제하며, 종이에 출력된 개인정보는 분쇄기로 분쇄하거나 소각을 통하여 파기합니다.
    
6. 개인정보의 안전성 확보 조치
회사는 개인정보보호법 제29조에 따라 다음과 같이 안전성 확보에 필요한 기술적/관리적 및 물리적 조치를 하고 있습니다.
    
- 개인정보 암호화
- 해킹 등에 대비한 기술적 대책
- 개인정보에 대한 접근 제한
- 문서보안을 위한 잠금장치 사용
- 비인가자에 대한 출입 통제
    
7. 개인정보 보호책임자
회사는 개인정보 처리에 관한 업무를 총괄해서 책임지고, 개인정보 처리와 관련한 정보주체의 불만처리 및 피해구제 등을 위하여 아래와 같이 개인정보 보호책임자를 지정하고 있습니다.
    
개인정보 수집 및 이용에 대한 동의를 거부할 권리가 있으며, 동의 거부 시 회원가입이 제한됩니다.
    
본 개인정보 수집 및 이용 동의서는 2024년 11월 9일부터 적용됩니다.`,
        agreed: false
    }
])

const allAgreed = ref(false)

const isAllAgreed = computed(() => {
    return terms.value.every(term => term.agreed)
})

const toggleAll = () => {
    terms.value.forEach(term => term.agreed = allAgreed.value)
}

const updateAgreement = () => {
    allAgreed.value = isAllAgreed.value
}

const proceedToSignup = () => {
    if (isAllAgreed.value) {
        router.push({ name: 'SignUpView' })
    }
}

// 줄바꿈 유지 함수
const formatContent = (content) => {
    return content.replace(/\n/g, '<br>')
}
</script>

<style scoped>
.terms-agreement {
    max-width: 37.5rem; /* 600px -> 37.5rem */
    margin: 0 auto;
    padding: 1.25rem; /* 20px -> 1.25rem */
}

.checkbox-group {
    margin-bottom: 1.25rem; /* 20px -> 1.25rem */
    padding-top: 1.875rem; /* 30px -> 1.875rem */
}

.additional-info {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    padding: 0.625rem; /* 10px -> 0.625rem */
    margin-bottom: 1.25rem; /* 20px -> 1.25rem */
    font-size: 0.9rem; /* 0.9em -> 0.9rem */
    line-height: 1.4;
}

.terms-content {
    border: 1px solid #ccc;
    padding: 0.625rem; /* 10px -> 0.625rem */
    margin-top: 0.625rem; /* 10px -> 0.625rem */
    height: 12.5rem; /* 200px -> 12.5rem */
    overflow-y: scroll;
    line-height: 1.6;
}

.button-container {
    display: flex;
    justify-content: center; /* 버튼 가운데 정렬 */
    padding-top: 3.125rem; /* 50px -> 3.125rem */
}

button {
    padding: 0.9375rem 1.875rem; /* 15px 30px -> 0.9375rem 1.875rem */
    font-size: 1.2rem; /* 1.2em -> 1.2rem */
    background-color: #000;
    color: #fff;
    border: none;
    border-radius: 0.3125rem; /* 5px -> 0.3125rem */
    cursor: pointer;
}

button:disabled {
    background-color: #ccc;
}
</style>
