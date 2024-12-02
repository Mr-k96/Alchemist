// stores/survey.js
import { defineStore } from 'pinia'

export const useSurveyStore = defineStore('survey', {
  state: () => ({
    investmentType: null
  }),
  
  actions: {
    setInvestmentType(value) {
      this.investmentType = value
    }
  },
  
  getters: {
    getInvestmentType: (state) => state.investmentType
  }
})