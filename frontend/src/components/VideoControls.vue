<script setup>
// Video player: open a file, play/pause, choose a frame with the slider, replay
// after the end, and use the current frame as the input image.
// Playback timing is a UI concern; every frame is read by the backend.
import { computed, onBeforeUnmount, ref } from 'vue'
import * as api from '../api.js'
import FramePreview from './FramePreview.vue'

const props = defineProps({ samples: Array })
const emit = defineEmits(['error', 'info', 'captured'])

const path = ref('')
const video = ref(null) // { frame_count, fps, width, height }
const index = ref(0)
const frame = ref(null)
const playing = ref(false)
let timer = null

const lastIndex = computed(() => (video.value ? video.value.frame_count - 1 : 0))
const ended = computed(() => video.value && index.value === lastIndex.value)
const videoSamples = computed(() => props.samples.filter((s) => /\.(avi|mp4|mkv|mov)$/i.test(s)))

async function showFrame(newIndex) {
  frame.value = await api.fetchVideoFrame(newIndex)
  index.value = newIndex
}

async function open() {
  pause()
  try {
    video.value = await api.openVideo(path.value)
    await showFrame(0)
    emit('info', `Opened video ${path.value}`)
  } catch (error) {
    video.value = null
    frame.value = null
    emit('error', error)
  }
}

// Shows the next frame, then schedules the following one so that frames
// appear every 1/fps seconds (or as fast as the backend can deliver them).
async function playStep() {
  if (!playing.value) return
  if (ended.value) {
    pause()
    return
  }
  const started = performance.now()
  try {
    await showFrame(index.value + 1)
  } catch (error) {
    pause()
    emit('error', error)
    return
  }
  const frameDuration = 1000 / video.value.fps
  const elapsed = performance.now() - started
  timer = setTimeout(playStep, Math.max(0, frameDuration - elapsed))
}

function play() {
  if (playing.value || ended.value) return
  playing.value = true
  playStep()
}

function pause() {
  playing.value = false
  clearTimeout(timer)
}

function replay() {
  pause()
  showFrame(0)
    .then(play)
    .catch((error) => emit('error', error))
}

function seek(event) {
  pause()
  showFrame(Number(event.target.value)).catch((error) => emit('error', error))
}

async function capture() {
  pause()
  try {
    emit('captured', await api.captureVideoFrame(index.value), `video frame ${index.value}`)
  } catch (error) {
    emit('error', error)
  }
}

onBeforeUnmount(pause)
</script>

<template>
  <div class="video">
    <form class="row" @submit.prevent="open">
      <input v-model="path" list="video-samples" placeholder="data/samples/ruch_testowy.avi" />
      <datalist id="video-samples">
        <option v-for="sample in videoSamples" :key="sample" :value="sample" />
      </datalist>
      <button type="submit">Open video</button>
    </form>

    <template v-if="video">
      <FramePreview :frame="frame" alt="Video frame" />
      <div class="row">
        <button v-if="ended" type="button" @click="replay">Replay</button>
        <button v-else-if="playing" type="button" @click="pause">Pause</button>
        <button v-else type="button" @click="play">Play</button>
        <input
          class="slider"
          type="range"
          min="0"
          :max="lastIndex"
          :value="index"
          aria-label="Frame"
          @change="seek"
        />
        <span class="counter">{{ index }} / {{ lastIndex }} ({{ video.fps.toFixed(1) }} fps)</span>
        <button type="button" @click="capture">Use frame as input</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.video {
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
input:not(.slider) {
  flex: 1 1 240px;
  min-width: 0;
}
.slider {
  flex: 1 1 200px;
}
.counter {
  font-family: ui-monospace, monospace;
  font-size: 0.9em;
}
</style>
