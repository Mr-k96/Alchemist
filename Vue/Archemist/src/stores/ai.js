import { defineStore } from 'pinia'

export const useAiStore = defineStore('ai', {
    state: () => ({
        analysisResult: null,
        loading: false,
        error: null
    }),
    
    actions: {
        setAnalysisResult(result) {
            try {
                this.analysisResult = result
                this.error = null
            } catch (error) {
                this.error = '분석 결과 처리 중 오류가 발생했습니다.'
                console.error('분석 결과 설정 오류:', error)
            }
        },
        
        setLoading(status) {
            this.loading = status
        },
        
        clearAnalysisResult() {
            this.analysisResult = null
            this.error = null
        },
        
        setError(error) {
            this.error = error
            this.loading = false
        }
    },
    
    getters: {
        hasAnalysisResult: (state) => !!state.analysisResult,
        isLoading: (state) => state.loading,
        getError: (state) => state.error
    }
})