// stores/maps.js
import { defineStore } from 'pinia'

export const useMapsStore = defineStore('maps', {
  state: () => ({
    map: null,
    markers: [],
    nearbyBanks: [],
    centerLat: 37.5665,
    centerLng: 126.9780,
    searchKeyword: '',
    loading: false,
    error: null
  }),

  actions: {
    async initializeMap(container) {
      try {
        const options = {
          center: new window.kakao.maps.LatLng(this.centerLat, this.centerLng),
          level: 3
        }
        this.map = new window.kakao.maps.Map(container, options)
      } catch (error) {
        console.error('지도 초기화 오류:', error)
        this.error = '지도를 불러오는데 실패했습니다.'
      }
    },

    async searchNearbyBanks() {
      if (!this.map) return

      this.loading = true
      try {
        const ps = new window.kakao.maps.services.Places(this.map)
        const restApiKey = import.meta.env.KAKAO_REST_API_KEY
        
        const searchResult = await new Promise((resolve, reject) => {
          ps.keywordSearch('은행 ' + this.searchKeyword, (data, status) => {
            if (status === window.kakao.maps.services.Status.OK) {
              resolve(data)
            } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
              resolve([])
            } else {
              reject(new Error('검색 중 오류가 발생했습니다.'))
            }
          }, {
            headers: {
              Authorization: `KakaoAK ${restApiKey}`
            }
          })
        })

        this.nearbyBanks = searchResult
        this.updateMarkers(searchResult)
      } catch (error) {
        console.error('검색 오류:', error)
        this.error = '은행 검색에 실패했습니다.'
      } finally {
        this.loading = false
      }
    },

    updateMarkers(places) {
      this.clearMarkers()
      if (places.length > 0) {
        const bounds = new window.kakao.maps.LatLngBounds()
        places.forEach(place => {
          const position = new window.kakao.maps.LatLng(place.y, place.x)
          const marker = this.createMarker(position)
          if (marker) {
            bounds.extend(position)
          }
        })
        this.map.setBounds(bounds)
      }
    },

    // ... 나머지 actions는 이전과 동일
  }
})