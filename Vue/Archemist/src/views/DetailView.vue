<template>
    <div>
      <h1>Detail</h1>
      <div v-if="article">
        <p>게시글 번호 : {{ article.id }}</p>
        <p>제목 : {{ article.title }}</p>
        <p>내용 : {{ article.content }}</p>
        <p>작성일 : {{ article.created_at }}</p>
        <p>수정일 : {{ article.updated_at }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from 'axios'
  import { onMounted, ref } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  import { useRoute } from 'vue-router'
  
  const store = useCounterStore()
  const route = useRoute()
  const article = ref(null)
  
  // DetailView가 마운트되기전에 DRF로 단일 게시글 조회를 요청 후 응답데이터를 저장
  onMounted(() => {
    axios({
      method: 'get',
      url: `${store.API_URL}/articles/${route.params.id}/`
    })
      .then((res) => {
        // console.log(res.data)
        article.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  })
  
  </script>
  
  <style>
  
  </style>
  