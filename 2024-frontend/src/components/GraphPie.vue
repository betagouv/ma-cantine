<script setup>
import { computed } from "vue"

const props = defineProps(["counts", "legends", "total"])
const colors = ["#A94645", "#C3992A", "134CB6A", "#FFCA00", "#695240"]

const stats = computed(() => {
  const unsortedStats = []
  for (let i = 0; i < props.counts.length; i++) {
    const percent = Math.round((props.counts[i] / props.total) * 100)
    if (percent !== 0) {
      const stat = {
        percent: percent,
        legend: props.legends[i],
        count: props.counts[i],
      }
      unsortedStats.push(stat)
    }
  }
  const descStats = unsortedStats.sort((first, second) => {
    if (second.count < first.count) return -1
    else if (second.count > first.count) return 1
    else return 0
  })
  return descStats
})

const background = computed(() => {
  const slices = []
  for (let i = 0; i < stats.value.length; i++) {
    const previousValue = i === 0 ? 0 : stats.value[i - 1].percent
    const currentValue = stats.value[i].percent
    const color = colors[i]
    slices.push(`${color} ${previousValue}% ${previousValue + currentValue}%`)
  }
  return `conic-gradient(${slices.join(",")})`
})
</script>
<template>
  <div class="graph-pie">
    <div class="graph-pie__circle" :style="`background: ${background}`"></div>
    <div class="graph-pie__legends-container">
      <div v-for="stat in stats" :key="stat" class="graph-pie__legend fr-mb-2w">
        <p class="fr-h6 fr-mb-1w">{{ stat.percent }}%</p>
        <p class="fr-mb-0">{{ stat.legend }}, soit {{ stat.count }} {{ stat.count > 1 ? "cantines" : "cantine" }}</p>
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
