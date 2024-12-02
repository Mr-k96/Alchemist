<template>
    <div>
      <h3>Finance List</h3>
      <FinanceListItem 
        v-for="finance in store.finances"
        :key="finance.id"
        :finance="finance"
      />
    </div>
  </template>
  
  <script setup>
  import FinanceListItem from '@/components/FinanceListItem.vue'
  import { useCounterStore } from '@/stores/counter'
  
  const store = useCounterStore()
  </script>
  