<script setup>
// Shows a frame given as a Blob; frees the previous object URL to avoid memory leaks.
import { onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({ frame: Blob, alt: String })
const url = ref(null)

watch(
  () => props.frame,
  (frame) => {
    if (url.value) URL.revokeObjectURL(url.value)
    url.value = frame ? URL.createObjectURL(frame) : null
  },
)

onBeforeUnmount(() => {
  if (url.value) URL.revokeObjectURL(url.value)
})
</script>

<template>
  <div class="frame">
    <img v-if="url" :src="url" :alt="alt" />
    <span v-else class="empty">No frame</span>
  </div>
</template>

<style scoped>
.frame {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 160px;
  background: #e4e7eb;
  border-radius: 6px;
  overflow: hidden;
}
img {
  max-width: 100%;
  max-height: 45vh;
  display: block;
}
.empty {
  color: #57606a;
}
</style>
