<script setup>
// Bar chart of a gray-level histogram (bins from black on the left to white on the right).
import { computed } from 'vue'

const props = defineProps({ histogram: Array })

const WIDTH = 256
const HEIGHT = 80

const bars = computed(() => {
  const highest = Math.max(...props.histogram, 1)
  const barWidth = WIDTH / props.histogram.length
  return props.histogram.map((count, bin) => {
    const height = (count / highest) * HEIGHT
    // Each bar is drawn in the gray level it represents.
    const gray = Math.round(((bin + 0.5) / props.histogram.length) * 255)
    return {
      x: bin * barWidth,
      y: HEIGHT - height,
      width: barWidth - 1,
      height,
      fill: `rgb(${gray}, ${gray}, ${gray})`,
    }
  })
})
</script>

<template>
  <svg :viewBox="`0 0 ${WIDTH} ${HEIGHT}`" class="histogram" role="img" aria-label="Histogram">
    <rect v-for="(bar, i) in bars" :key="i" v-bind="bar" stroke="#8c959f" stroke-width="0.5" />
  </svg>
</template>

<style scoped>
.histogram {
  width: 100%;
  height: 80px;
  background: #fff7e0;
  border-radius: 4px;
}
</style>
