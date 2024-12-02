import { defineStore } from 'pinia';
import axios from 'axios';

export const useExchangeRateStore = defineStore('exchangeRate', {
    state: () => ({
        exchangeRates: null, // 환율 데이터
    }),
    actions: {
        async fetchExchangeRates() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/exchange_rate/');
                this.exchangeRates = response.data;
                if (!Array.isArray(this.exchangeRates) || this.exchangeRates.length === 0) {
                    throw new Error('환율 데이터가 비어 있습니다.');
                }
                return this.exchangeRates;
            } catch (error) {
                console.error('환율 데이터를 가져오는 데 실패했습니다:', error);
                throw new Error('환율 데이터를 가져오는 데 실패했습니다.');
            }
        },
        async getExchangeRate(baseCurrency, targetCurrency) {
            if (!this.exchangeRates) {
                await this.fetchExchangeRates();
            }

            const baseRate = this.exchangeRates.find(rate => rate.cur_unit === baseCurrency);
            const targetRate = this.exchangeRates.find(rate => rate.cur_unit === targetCurrency);

            if (!baseRate || !targetRate) {
                console.error('환율 데이터를 찾을 수 없습니다.');
                return null;
            }

            console.log(`Base: ${baseRate.cur_unit} (${baseRate.deal_bas_r}), Target: ${targetRate.cur_unit} (${targetRate.deal_bas_r})`);

            return parseFloat(targetRate.deal_bas_r) / parseFloat(baseRate.deal_bas_r);
        }
    }
});
