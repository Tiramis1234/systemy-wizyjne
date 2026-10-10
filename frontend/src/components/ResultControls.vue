<script setup>
// Choosing the operation that produces the result, and resetting the result.
import { ref } from 'vue'

defineProps({ disabled: Boolean })
const emit = defineEmits(['apply', 'reset'])

// Values must match app/core/operations.py::Operation.
const operations = [
  { value: 'none', label: 'None (copy of input)' },
  { value: 'grayscale', label: 'Grayscale' },
]
const operation = ref('grayscale')
</script>

<template>
  <div class="controls">
    <label>
      Operation
      <select v-model="operation" :disabled="disabled">
        <option v-for="op in operations" :key="op.value" :value="op.value">{{ op.label }}</option>
      </select>
    </label>
    <button type="button" :disabled="disabled" @click="emit('apply', operation)">Apply</button>
    <button type="button" :disabled="disabled" @click="emit('reset')">Reset</button>
  </div>
</template>

<style scoped>
.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
</style>
