<script setup>
// Choosing the operation that produces the result, resetting and saving it.
import { ref } from 'vue'
import { resultDownloadUrl } from '../api.js'

defineProps({ disabled: Boolean })
const emit = defineEmits(['apply', 'reset', 'save'])

// Values must match app/core/operations.py::Operation.
const operations = [
  { value: 'none', label: 'None (copy of input)' },
  { value: 'grayscale', label: 'Grayscale' },
]
const operation = ref('grayscale')

// Saved on the server; the extension (.png / .jpg) picks the format.
const savePath = ref('output/result.png')
</script>

<template>
  <div class="rows">
    <div class="row">
      <label>
        Operation
        <select v-model="operation" :disabled="disabled">
          <option v-for="op in operations" :key="op.value" :value="op.value">
            {{ op.label }}
          </option>
        </select>
      </label>
      <button type="button" :disabled="disabled" @click="emit('apply', operation)">Apply</button>
      <button type="button" :disabled="disabled" @click="emit('reset')">Reset</button>
    </div>
    <form class="row" @submit.prevent="emit('save', savePath)">
      <input v-model="savePath" :disabled="disabled" aria-label="Save path" />
      <button type="submit" :disabled="disabled">Save on server</button>
      <template v-if="!disabled">
        <a :href="resultDownloadUrl('png')" download>Download PNG</a>
        <a :href="resultDownloadUrl('jpg')" download>Download JPG</a>
      </template>
    </form>
  </div>
</template>

<style scoped>
.rows {
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
input {
  flex: 1 1 240px;
  min-width: 0;
}
</style>
