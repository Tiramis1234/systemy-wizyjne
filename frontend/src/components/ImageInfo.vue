<script setup>
defineProps({ info: Object }) // { width, height, channels, dtype } or null
</script>

<template>
  <dl v-if="info" class="info">
    <dt>Resolution</dt>
    <dd>{{ info.width }} × {{ info.height }} px</dd>
    <dt>Channels</dt>
    <dd>{{ info.channels }}</dd>
    <dt>Data type</dt>
    <dd>{{ info.dtype }}</dd>
  </dl>
</template>

<style scoped>
.info {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 2px 12px;
  margin: 8px 0 0;
  font-size: 0.9em;
}
dt {
  color: #57606a;
}
dd {
  margin: 0;
  font-family: ui-monospace, monospace;
}
</style>
