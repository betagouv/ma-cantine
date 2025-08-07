<script setup>
import { computed } from "vue"

const props = defineProps(["stats", "legends"])
const colors = ["#A94645", "#C3992A", "#695240"]
const statsOrderedDesc = computed(() => {
  const unsortedArray = [...props.stats]
  const sortedArray = unsortedArray.sort((first, second) => {
    if (second < first) return -1
    else if (second > first) return 1
    else return 0
  })
  return sortedArray
})

const findLegend = (value) => {
  const unorderedIndex = props.stats.indexOf(value)
  return props.legends[unorderedIndex]
}

const generateBackground = () => {
  const slices = []
  for (let i = 0; i < statsOrderedDesc.value.length; i++) {
    const previousValue = i === 0 ? 0 : statsOrderedDesc.value[i - 1]
    const currentValue = statsOrderedDesc.value[i]
    const color = colors[i]
    slices.push(`${color} ${previousValue}% ${previousValue + currentValue}%`)
  }
  return `conic-gradient(${slices.join(",")})`
}
</script>
<template>
  <div class="graph-pie">
    <div class="graph-pie__circle" :style="`background: ${generateBackground()}`"></div>
    <div class="graph-pie__legends-container">
      <div v-for="(value, index) in statsOrderedDesc" :key="index" class="graph-pie__legend fr-mb-2w">
        <p class="fr-h6 fr-mb-1w">{{ value }}%</p>
        <p class="fr-mb-0">{{ findLegend(value) }}</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.graph-pie {
  display: flex;
  gap: 2rem;
  flex-direction: column;
  align-items: center;

  @media (min-width: 768px) {
    align-items: center;
    flex-direction: row;
  }

  &__circle {
    flex-shrink: 0;
    width: 10rem;
    height: 10rem;
    border-radius: 100%;
    overflow: hidden;
  }

  &__legends-container {
    align-self: flex-start;
  }
}
</style>
