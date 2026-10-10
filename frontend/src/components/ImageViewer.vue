<script setup>
import ImageInfo from './ImageInfo.vue'

defineProps({
  title: String,
  src: String, // null when there is no image yet
  info: Object,
})
</script>

<template>
  <section class="viewer">
    <h2>{{ title }}</h2>
    <div class="frame">
      <img v-if="src" :src="src" :alt="title" />
      <span v-else class="empty">No image</span>
    </div>
    <ImageInfo :info="info" />
  </section>
</template>

<style scoped>
.viewer {
  flex: 1 1 320px;
  min-width: 0;
}
h2 {
  font-size: 1em;
  margin: 0 0 6px;
}
.frame {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  background: #e4e7eb;
  border-radius: 6px;
  overflow: hidden;
}
img {
  max-width: 100%;
  max-height: 60vh;
  display: block;
}
.empty {
  color: #57606a;
}
</style>
