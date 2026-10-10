<script setup>
// Shows the last success or error message. Errors stay until dismissed.
defineProps({ message: Object }) // { kind: 'error' | 'info', text: string } or null
defineEmits(['dismiss'])
</script>

<template>
  <div v-if="message" class="message" :class="message.kind" role="status">
    <span>{{ message.text }}</span>
    <button type="button" @click="$emit('dismiss')">×</button>
  </div>
</template>

<style scoped>
.message {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  margin-bottom: 12px;
  border-radius: 6px;
}
.error {
  background: #fde8e8;
  color: #8a1c1c;
}
.info {
  background: #e7f3ec;
  color: #1d5b34;
}
button {
  border: none;
  background: none;
  font-size: 1.2em;
  cursor: pointer;
  color: inherit;
}
</style>
