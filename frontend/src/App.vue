<script setup>
import { onMounted, ref } from 'vue'
import * as api from './api.js'
import CameraControls from './components/CameraControls.vue'
import ImageSourceControls from './components/ImageSourceControls.vue'
import ImageViewer from './components/ImageViewer.vue'
import MessageBar from './components/MessageBar.vue'
import ResultControls from './components/ResultControls.vue'
import VideoControls from './components/VideoControls.vue'

const samples = ref([])
const sourceTab = ref('image') // 'image' | 'video' | 'camera'
const sourceTabs = [
  { value: 'image', label: 'Image file' },
  { value: 'video', label: 'Video file' },
  { value: 'camera', label: 'Camera' },
]
const message = ref(null)

const inputInfo = ref(null)
const inputVersion = ref(0) // bumped after every change, forces the <img> to reload
const resultInfo = ref(null)
const resultVersion = ref(0)

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

function onResultChanged(info) {
  resultInfo.value = info
  resultVersion.value += 1
}

// A new input always resets the result to a copy of it (see Workspace.set_input).
function onInputLoaded(info, sourceName) {
  inputInfo.value = info
  inputVersion.value += 1
  onResultChanged(info)
  showInfo(`Loaded ${sourceName}`)
}

function loadPath(path) {
  run(async () => onInputLoaded(await api.loadImageFromPath(path), path))
}

function upload(file) {
  run(async () => onInputLoaded(await api.uploadImage(file), file.name))
}

function applyOperation(operation) {
  run(async () => {
    onResultChanged(await api.applyOperation(operation))
    showInfo(`Applied: ${operation}`)
  })
}

function resetResult() {
  run(async () => {
    onResultChanged(await api.resetResult())
    showInfo('Result reset to input')
  })
}

function saveResult(path) {
  run(async () => {
    const saved = await api.saveResult(path)
    showInfo(`Saved result to ${saved.path}`)
  })
}

onMounted(() => run(async () => (samples.value = await api.listSamples())))
</script>

<template>
  <main>
    <h1>Machine Vision Systems</h1>
    <MessageBar :message="message" @dismiss="message = null" />

    <section class="panel">
      <nav class="tabs">
        <button
          v-for="tab in sourceTabs"
          :key="tab.value"
          type="button"
          :class="{ active: sourceTab === tab.value }"
          @click="sourceTab = tab.value"
        >
          {{ tab.label }}
        </button>
      </nav>
      <ImageSourceControls
        v-show="sourceTab === 'image'"
        :samples="samples"
        @load-path="loadPath"
        @upload="upload"
      />
      <VideoControls
        v-show="sourceTab === 'video'"
        :samples="samples"
        @error="showError"
        @info="showInfo"
        @captured="onInputLoaded"
      />
      <CameraControls
        v-show="sourceTab === 'camera'"
        @error="showError"
        @info="showInfo"
        @captured="onInputLoaded"
      />
    </section>

    <section class="panel">
      <ResultControls
        :disabled="!inputInfo"
        @apply="applyOperation"
        @reset="resetResult"
        @save="saveResult"
      />
    </section>

    <div class="viewers">
      <ImageViewer
        title="Input"
        :src="inputInfo ? api.inputImageUrl(inputVersion) : null"
        :info="inputInfo"
      />
      <ImageViewer
        title="Result"
        :src="resultInfo ? api.resultImageUrl(resultVersion) : null"
        :info="resultInfo"
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
.tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 10px;
}
.tabs button {
  border: 1px solid #8c959f;
  background: white;
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
}
.tabs button.active {
  background: #1f2328;
  color: white;
}
.viewers {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
</style>
