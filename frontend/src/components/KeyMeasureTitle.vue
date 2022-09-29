<template>
  <div v-if="measure">
    <span :class="`icon ${measure.iconClass}`"></span>
    <span class="ml-4">{{ measure.title }}</span>
  </div>
</template>

<script>
export default {
  name: "KeyMeasureTitle",
  props: {
    measure: Object,
  },
}
</script>

<style scoped>
.icon,
.icon::before {
  --icon-size: 2.5rem;
  --font-size: 1.75rem;
}
</style>
