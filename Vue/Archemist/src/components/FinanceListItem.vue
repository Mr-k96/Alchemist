<template>
    <div>
      <h5>{{ finance.id }}</h5>
      <p>{{ finance.title }}</p>
      <p>{{ finance.content }}</p>
      <RouterLink 
        :to="{ name: 'DetailView', params: { id: finance.id } }"  
      >
        Detail
      </RouterLink>
      <hr>
    </div>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router'
  
  defineProps({
    finance: Object
  })
  </script>
  
  