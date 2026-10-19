<script setup>
// Lighting comparison: store the current input as A or B (e.g. lamp off / lamp on)
// and compare brightness statistics computed by the backend.
import { ref } from 'vue'
import * as api from '../api.js'
import HistogramChart from './HistogramChart.vue'

defineProps({ disabled: Boolean })
const emit = defineEmits(['error', 'info'])

const comparison = ref({ A: null, B: null, mean_difference: null })
const version = ref(0)
const slots = ['A', 'B']

function percent(fraction) {
  return `${(fraction * 100).toFixed(1)} %`
}

async function store(slot) {
  try {
    await api.storeComparisonSlot(slot)
    comparison.value = await api.getComparison()
    version.value += 1
    emit('info', `Current input stored as ${slot}`)
  } catch (error) {
    emit('error', error)
  }
}
</script>

<template>
  <section class="compare">
    <h2>Lighting comparison</h2>
    <p class="hint">
      Capture a frame under lighting A, store it as A; change only the lighting, capture again,
      store as B.
    </p>
    <div class="buttons">
      <button v-for="slot in slots" :key="slot" type="button" :disabled="disabled" @click="store(slot)">
        Store input as {{ slot }}
      </button>
    </div>
    <div class="columns">
      <div v-for="slot in slots" :key="slot" class="column">
        <h3>{{ slot }}</h3>
        <template v-if="comparison[slot]">
          <img :src="api.comparisonImageUrl(slot, version)" :alt="`Snapshot ${slot}`" />
          <HistogramChart :histogram="comparison[slot].histogram" />
          <dl>
            <dt>Mean brightness</dt>
            <dd>{{ comparison[slot].mean.toFixed(1) }}</dd>
            <dt>Std (contrast)</dt>
            <dd>{{ comparison[slot].std.toFixed(1) }}</dd>
            <dt>Min / max</dt>
            <dd>{{ comparison[slot].min }} / {{ comparison[slot].max }}</dd>
            <dt>Dark pixels (≤ 5)</dt>
            <dd>{{ percent(comparison[slot].dark_fraction) }}</dd>
            <dt>Bright pixels (≥ 250)</dt>
            <dd>{{ percent(comparison[slot].bright_fraction) }}</dd>
          </dl>
        </template>
        <span v-else class="empty">Not stored yet</span>
      </div>
    </div>
    <p v-if="comparison.mean_difference !== null" class="difference">
      Mean brightness B − A: <strong>{{ comparison.mean_difference.toFixed(1) }}</strong>
      ({{ comparison.mean_difference >= 0 ? 'B is brighter' : 'A is brighter' }})
    </p>
  </section>
</template>

<style scoped>
.compare {
  background: white;
  border-radius: 6px;
  padding: 12px;
  margin-top: 16px;
}
h2 {
  font-size: 1em;
  margin: 0 0 4px;
}
h3 {
  margin: 0 0 6px;
}
.hint {
  margin: 0 0 8px;
  color: #57606a;
  font-size: 0.9em;
}
.buttons {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}
.columns {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.column {
  flex: 1 1 280px;
  min-width: 0;
}
img {
  max-width: 100%;
  display: block;
  margin-bottom: 6px;
  border-radius: 4px;
}
dl {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 2px 12px;
  font-size: 0.9em;
}
dt {
  color: #57606a;
}
dd {
  margin: 0;
  font-family: ui-monospace, monospace;
}
.empty {
  color: #57606a;
}
</style>
