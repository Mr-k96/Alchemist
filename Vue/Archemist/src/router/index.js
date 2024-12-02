import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import FinanceView from '@/views/FinanceView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import { useCounterStore } from '@/stores/counter'
import UserProfile from '@/views/UserProfile.vue'
import TermsAgreementView from '@/views/TermsAgreementView.vue'
import InvestmentSurveyView from '@/views/InvestmentSurveyView.vue'
import PreferAssetView from '@/views/PreferAssetView.vue'
import ReportView from '@/views/ReportView.vue'
import AiReportView from '@/views/AiReportView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView', // 홈 페이지 라우트 이름
      component: HomeView // Home 컴포넌트 연결
    },
    {
      path: '/about',
      name: 'AboutView', // About 페이지 라우트 이름
      component: AboutView // About 컴포넌트 연결
    },
    {
      path: '/finances',
      name: 'FinanceView',
      component: FinanceView
    },
    {
      path: '/finances/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/terms-agreement',
      name: 'TermsAgreement',
      component: TermsAgreementView
    },
    {
      path: '/profile',
      name: 'Profile',
      component: UserProfile,
      meta: { requiresAuth: true }
    },
    {
      path: '/survey',
      name: 'InvestmentSurvey',
      component: InvestmentSurveyView
    },
    {
      path: '/prefer-asset',
      name: 'PreferAsset',
      component: PreferAssetView,
      meta: { requiresAuth: true }
    },
    {
      path: '/report',
      name: 'Report',
      component: ReportView,
      meta: { requiresAuth: true }
    },
    {
      path: '/ai_report',
      name: 'AiReport',
      component: AiReportView,
      meta: { requiresAuth: true }
    },
  ]
})

router.beforeEach((to, from) => {
  const store = useCounterStore()
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (to.name === 'FinanceView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

    if (to.meta.requiresAuth && !store.isLogin) {
    window.alert('로그인이 필요한 페이지입니다.')
    return { name: 'LogInView' }
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin)) {
    window.alert('이미 로그인 되어있습니다.')
    return { name: 'FinanceView' }
  }

  return true
})

export default router
