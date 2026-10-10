<script setup>
import { onMounted, ref } from 'vue'
import * as api from './api.js'
import ImageSourceControls from './components/ImageSourceControls.vue'
import ImageViewer from './components/ImageViewer.vue'
import MessageBar from './components/MessageBar.vue'

const samples = ref([])
const message = ref(null)

const inputInfo = ref(null)
const inputVersion = ref(0) // bumped after every change, forces the <img> to reload

function showError(error) {
  message.value = { kind: 'error', text: error.message }
}

function showInfo(text) {
  message.value = { kind: 'info', text }
}

// Runs an API call; errors become a message instead of breaking the interface.
async function run(action) {
  try {
    await action()
  } catch (error) {
    showError(error)
  }
}

function onInputLoaded(info, sourceName) {
  inputInfo.value = info
  inputVersion.value += 1
  showInfo(`Loaded ${sourceName}`)
}

function loadPath(path) {
  run(async () => onInputLoaded(await api.loadImageFromPath(path), path))
}

function upload(file) {
  run(async () => onInputLoaded(await api.uploadImage(file), file.name))
}

onMounted(() => run(async () => (samples.value = await api.listSamples())))
</script>

<template>
  <main>
    <h1>Machine Vision Systems</h1>
    <MessageBar :message="message" @dismiss="message = null" />

    <section class="panel">
      <ImageSourceControls :samples="samples" @load-path="loadPath" @upload="upload" />
    </section>

    <div class="viewers">
      <ImageViewer
        title="Input"
        :src="inputInfo ? api.inputImageUrl(inputVersion) : null"
        :info="inputInfo"
      />
    </div>
  </main>
</template>

<style scoped>
h1 {
  font-size: 1.4em;
  margin: 0 0 12px;
}
.panel {
  background: white;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 12px;
}
.viewers {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
</style>
