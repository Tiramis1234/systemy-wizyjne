<script setup>
// Live camera preview: start (open the device), capture the current frame as
// input, stop (release the device so other programs can use it).
import { onBeforeUnmount, ref } from 'vue'
import * as api from '../api.js'
import FramePreview from './FramePreview.vue'

const emit = defineEmits(['error', 'info', 'captured'])

// Target preview rate. 15 fps is smooth enough to aim the camera while keeping
// the load low (every frame travels through the backend as PNG).
const PREVIEW_FPS = 15

const index = ref(0) // 0 = first camera (/dev/video0)
const running = ref(false)
const size = ref(null) // { width, height }
const frame = ref(null)
let timer = null

// Fetches one frame, then schedules the next; stops on the first error.
async function previewStep() {
  if (!running.value) return
  const started = performance.now()
  try {
    frame.value = await api.fetchCameraFrame()
  } catch (error) {
    stopPreview()
    emit('error', error)
    return
  }
  const elapsed = performance.now() - started
  timer = setTimeout(previewStep, Math.max(0, 1000 / PREVIEW_FPS - elapsed))
}

function stopPreview() {
  running.value = false
  clearTimeout(timer)
}

async function start() {
  stopPreview()
  try {
    size.value = await api.openCamera(index.value)
    running.value = true
    emit('info', `Camera ${index.value} opened (${size.value.width} × ${size.value.height})`)
    previewStep()
  } catch (error) {
    size.value = null
    frame.value = null
    emit('error', error)
  }
}

async function stop() {
  stopPreview()
  try {
    await api.closeCamera()
    emit('info', 'Camera released')
  } catch (error) {
    emit('error', error)
  }
}

async function capture() {
  try {
    emit('captured', await api.captureCameraFrame(), `camera ${index.value} frame`)
  } catch (error) {
    emit('error', error)
  }
}

onBeforeUnmount(stopPreview)
</script>

<template>
  <div class="camera">
    <div class="row">
      <label>
        Camera index
        <input v-model.number="index" type="number" min="0" :disabled="running" />
      </label>
      <button v-if="!running" type="button" @click="start">Start</button>
      <template v-else>
        <button type="button" @click="capture">Capture frame as input</button>
        <button type="button" @click="stop">Stop</button>
      </template>
    </div>
    <FramePreview v-if="running || frame" :frame="frame" alt="Camera preview" />
  </div>
</template>

<style scoped>
.camera {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
input[type='number'] {
  width: 4em;
}
</style>
