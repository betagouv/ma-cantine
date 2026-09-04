<script setup>
import { computed } from "vue"
import stringsService from "@/services/strings"

const props = defineProps(["percents", "legends", "alignment"])
const colors = ["#A94645", "#C3992A", "#695240", "#FFCA00", "#34CB6A", "#FF9575", "#297254", "#CE614A"]

const stats = computed(() => {
  const formattedStats = []
  for (let i = 0; i < props.percents.length; i++) {
    const stat = {
      percent: props.percents[i],
      legend: props.legends[i],
    }
    formattedStats.push(stat)
  }
  const descStats = formattedStats.sort((first, second) => {
    if (second.percent < first.percent) return -1
    else if (second.percent > first.percent) return 1
    else return 0
  })
  return descStats
})

const background = computed(() => {
  const slices = []
  let previousValue = 0
  for (let i = 0; i < stats.value.length; i++) {
    const currentValue = stats.value[i].percent
    const nextValue = previousValue + currentValue
    const color = colors[i]
    slices.push(`${color} ${previousValue}% ${nextValue}%`)
    previousValue = nextValue
  }
  return `conic-gradient(${slices.join(",")})`
})
</script>
<template>
  <div class="graph-pie fr-mt-4w fr-mb-3w">
    <div class="graph-pie__circle" :style="`background: ${background}`"></div>
    <div :class="`graph-pie__legends-container graph-pie__legends-container--${alignment || 'vertical'}`">
      <div v-for="(stat, i) in stats" :key="stat" class="graph-pie__legend">
        <div class="graph-pie__color fr-mr-1w" :style="`background-color: ${colors[i]}`"></div>
        <div>
          <p class="fr-h6 fr-mb-0">{{ stringsService.prettyPercent(stat.percent) }}</p>
          <p class="fr-mb-0">{{ stat.legend }}</p>
        </div>
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
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 2rem;
    width: 100%;

    &--horizontal {
      flex-direction: row;
      flex-wrap: wrap;
    }
  }

  &__legend {
    display: flex;
  }

  &__color {
    width: 0.5rem;
    flex-shrink: 0;
  }
}
</style>
