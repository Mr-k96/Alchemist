<template>
  <div id="app">
    <NavBar />
    <RouterView />
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterView } from "vue-router"
import NavBar from "@/components/NavBar.vue"
import Footer from "@/components/Footer.vue"
import axios from "axios"

const dataList = ref([])

const fetchData = (condition) => {
  axios({
    method: "GET",
    url: "http://localhost:8000/ETF/etf-list/",
    params: condition
  })
    .then(response => {
      dataList.value = response.data
    })
    .catch(error => {
      console.error("데이터 조회 실패:", error)
    })
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>

</style>