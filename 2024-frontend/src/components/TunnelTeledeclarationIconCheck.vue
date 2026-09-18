<script setup>
import { computed } from "vue"

const props = defineProps(["isComplete"])
const iconClasses = computed(() => {
  const color = props.isComplete ? "default--success" : "mention--grey"
  const shape = props.isComplete ? "fill" : "line"
  return `fr-icon-checkbox-circle-${shape} fr-text-${color}`
})
</script>

<template>
  <span :class="iconClasses" class="ma-cantine--icon-xs"></span>
</template>
