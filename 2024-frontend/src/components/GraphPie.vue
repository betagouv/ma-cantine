<script setup>
const props = defineProps(["stats"])
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
  </div>
</template>

<style lang="scss">
.graph-pie {
  &__circle {
    width: 5rem;
    height: 5rem;
    border-radius: 100%;
    overflow: hidden;
  }
}
</style>
