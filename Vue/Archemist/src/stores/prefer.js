import { defineStore } from 'pinia'
import axios from 'axios'

export const usePreferStore = defineStore('prefer', {
  state: () => ({
    etfList: [],
    filters: {
      risks: [],
      markets: [],
      assets: [],
      stock_options: [],
      bond_options: [],
      industries: [],
      managers: [],
    },
    selectedShortCodes: [],
    selectedEtfList: []
  }),

  actions: {
    async fetchEtfList() {
      try {
        const response = await axios.get('http://localhost:8000/ETF/etf-list/', {
          headers: {
            'Content-Type': 'application/json',
          }
        });
        this.etfList = response.data || []; // null 체크 추가
      } catch (error) {
        console.error('데이터 조회 실패:', error);
        if (error.response) {
          console.error('에러 상세:', error.response.data);
        }
        this.etfList = [];
      }
    },

    async applyFilters() {
      try {
        const filterData = {
          risks: this.filters.risks,
          markets: this.filters.markets,
          assets: this.filters.assets,
          stock_options: this.filters.assets.includes('주식') ? this.filters.stock_options : [],
          bond_options: this.filters.assets.includes('채권') ? this.filters.bond_options : [],
          industries: this.filters.assets.includes('주식') ? this.filters.industries : [],
          managers: this.filters.managers,
          asset_relation: 'OR'
        };
    
        const response = await axios({
          method: 'post',
          url: 'http://localhost:8000/ETF/etf-list/',
          data: filterData,
          headers: {
            'Content-Type': 'application/json'
          },
          validateStatus: function (status) {
            return status >= 200 && status < 300;
          }
        });
        
        if (response.data) {
          this.etfList = response.data;
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    
    // 에러 처리 메서드 추가
    handleError(error) {
      console.error('필터링 실패:', error);
      if (error.response) {
        console.error('에러 상태:', error.response.status);
        console.error('에러 상세:', error.response.data);
      } else if (error.request) {
        console.error('응답 없음:', error.request);
      } else {
        console.error('요청 설정 중 에러:', error.message);
      }
    },

    // ETF 선택 관련 액션 추가
    updateSelectedEtf(etf) {
      const index = this.selectedEtfList.findIndex(item => item.short_code === etf.short_code);
      if (index === -1) {
        this.selectedEtfList.push(etf);
        this.selectedShortCodes.push(etf.short_code);
      } else {
        this.selectedEtfList.splice(index, 1);
        const codeIndex = this.selectedShortCodes.indexOf(etf.short_code);
        if (codeIndex > -1) {
          this.selectedShortCodes.splice(codeIndex, 1);
        }
      }
    },

    setSelectedShortCodes() {
      this.selectedShortCodes = this.etfList.map(etf => etf.short_code)
    },

    clearSelectedShortCodes() {
      this.selectedShortCodes = []
    },

    // 필터 초기화 액션 추가
    resetFilters() {
      this.filters = {
        risks: [],
        markets: [],
        assets: [],
        stock_options: [],
        bond_options: [],
        industries: [],
        managers: []
      }
    }
  },
  
  getters: {
    getSelectedShortCodes: (state) => state.selectedShortCodes,
    selectedShortCodesCount: (state) => state.selectedShortCodes.length,
    isEtfSelected: (state) => (shortCode) => {
      return state.selectedShortCodes.includes(shortCode);
    }
  }
})