<script setup>
const props = defineProps(["stats", "legends"])
const colors = ["#A94645", "#C3992A", "#695240"]

const generateBackground = () => {
  const slices = []
  for (let i = 0; i < props.stats.length; i++) {
    const previousValue = i === 0 ? 0 : props.stats[i - 1]
    const currentValue = props.stats[i]
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
      <div v-for="(legend, index) in legends" :key="index" class="graph-pie__legend fr-mb-2w">
        <p class="fr-h6 fr-mb-1w">{{ stats[index] }}%</p>
        <p class="fr-mb-0">{{ legend }}</p>
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
