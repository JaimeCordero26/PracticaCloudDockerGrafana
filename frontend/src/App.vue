<template>
  <div>
    <h1>Vue + Django + Docker</h1>
    <button @click="fetchHello">Probar API Django</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const message = ref('')
async function fetchHello() {
  try {
    const res = await fetch('http://localhost:8000/api/hello/')
    const data = await res.json()
    message.value = data.message
  } catch {
    message.value = 'No se pudo conectar a Django.'
  }
}
</script>
