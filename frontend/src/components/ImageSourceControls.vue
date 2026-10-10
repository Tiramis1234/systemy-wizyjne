<script setup>
// Loading a still image: by a path on the server (with sample suggestions) or by upload.
import { ref } from 'vue'

const props = defineProps({ samples: Array })
const emit = defineEmits(['load-path', 'upload'])

const path = ref('')

function onFileChosen(event) {
  const file = event.target.files[0]
  if (file) emit('upload', file)
  event.target.value = '' // allow choosing the same file again
}

function imageSamples() {
  return props.samples.filter((sample) => /\.(png|jpe?g)$/i.test(sample))
}
</script>

<template>
  <div class="controls">
    <form @submit.prevent="emit('load-path', path)">
      <input v-model="path" list="image-samples" placeholder="data/samples/obraz_testowy.png" />
      <datalist id="image-samples">
        <option v-for="sample in imageSamples()" :key="sample" :value="sample" />
      </datalist>
      <button type="submit">Load from path</button>
    </form>
    <label class="upload">
      Upload JPG/PNG
      <input type="file" accept=".png,.jpg,.jpeg" @change="onFileChosen" />
    </label>
  </div>
</template>

<style scoped>
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
form {
  display: flex;
  gap: 8px;
  flex: 1 1 320px;
}
input:not([type='file']) {
  flex: 1;
  min-width: 0;
}
.upload input {
  display: none;
}
.upload {
  padding: 4px 10px;
  border: 1px solid #8c959f;
  border-radius: 4px;
  cursor: pointer;
  background: white;
}
</style>
