<script setup>
import { onMounted, ref } from 'vue'

const backendStatus = ref('checking...')

onMounted(async () => {
  try {
    const response = await fetch('/api/health')
    backendStatus.value = response.ok ? 'ok' : `error ${response.status}`
  } catch {
    backendStatus.value = 'unreachable'
  }
})
</script>

<template>
  <main>
    <h1>Machine Vision Systems</h1>
    <p>Backend: {{ backendStatus }}</p>
  </main>
</template>
