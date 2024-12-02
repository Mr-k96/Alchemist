import { defineStore } from "pinia";
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const useEtfStore = defineStore("etf", {
  state: () => ({
    assets: [],
    filteredAssets: [],
    loading: false,
    error: null,
  }),

  getters: {
    getAssetCount: (state) => state.assets.length,
    getFilteredCount: (state) => state.filteredAssets.length,
  },

  actions: {
    async fetchEtfData() {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.get("/ETF/etf-list/");
        
        if (!response.data) {
          throw new Error('데이터를 불러올 수 없습니다.');
        }

        // 데이터 구조 확인 및 처리
        const etfData = Array.isArray(response.data) ? response.data : response.data.results;
        
        if (!etfData || etfData.length === 0) {
          throw new Error('ETF 데이터가 없습니다.');
        }

        // 데이터 정제
        this.assets = etfData.map(asset => ({
          ...asset,
          name: asset.name || '이름 없음',
          manager: asset.manager || '운용사 정보 없음',
          market_category: asset.market_category || '분류 없음',
          asset_category: asset.asset_category || '분류 없음',
          risk_level: asset.risk_level || '정보 없음',
        }));
        
        this.filteredAssets = [...this.assets];
      } catch (err) {
        this.error = err.message || "ETF 정보를 불러오는데 실패했습니다.";
        console.error("API Error:", err);
      } finally {
        this.loading = false;
      }
    },

    searchAssets(searchTerm) {
      try {
        if (!this.assets.length) {
          this.filteredAssets = [];
          return;
        }

        if (!searchTerm || !searchTerm.trim()) {
          this.filteredAssets = [...this.assets];
          return;
        }

        const searchLower = searchTerm.toLowerCase().trim();
        this.filteredAssets = this.assets.filter(asset => {
          return asset && (
            (asset.name?.toLowerCase().includes(searchLower)) ||
            (asset.manager?.toLowerCase().includes(searchLower)) ||
            (asset.market_category?.toLowerCase().includes(searchLower)) ||
            (asset.asset_category?.toLowerCase().includes(searchLower))
          );
        });
      } catch (err) {
        console.error("Search Error:", err);
        this.error = "검색 중 오류가 발생했습니다.";
      }
    },

    resetFilters() {
      this.filteredAssets = [...this.assets];
      this.error = null;
    },

    filterByRiskLevel(riskLevel) {
      try {
        if (!riskLevel) {
          this.filteredAssets = [...this.assets];
          return;
        }
        this.filteredAssets = this.assets.filter(
          asset => asset.risk_level === riskLevel
        );
      } catch (err) {
        console.error("Risk Level Filter Error:", err);
        this.error = "위험도 필터링 중 오류가 발생했습니다.";
      }
    },

    filterByManager(manager) {
      try {
        if (!manager) {
          this.filteredAssets = [...this.assets];
          return;
        }
        this.filteredAssets = this.assets.filter(
          asset => asset.manager === manager
        );
      } catch (err) {
        console.error("Manager Filter Error:", err);
        this.error = "운용사 필터링 중 오류가 발생했습니다.";
      }
    },
  },
});