<script setup>
import { computed } from "vue"

const props = defineProps(["emphasisText", "contextText", "color"])

const highlightColor = computed(() => props.color || "defaultColor")
</script>

<template>
  <p :class="`fr-my-4w highlight ${highlightColor}`">
    <span class="fr-h3">{{ emphasisText }}</span>
    {{ contextText }}
  </p>
</template>

<style scoped>
p.highlight {
  color: var(--text-mention-grey);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
p.highlight > span {
  border-radius: 18px;
  padding: 4px 16px;
  margin-right: 8px;
  margin-bottom: 0;

  background: var(--background-default-grey-hover);
  color: inherit;
}
p.highlight.brown {
  color: var(--text-action-high-orange-terre-battue);
}
p.highlight.brown > span {
  background: var(--orange-terre-battue-975-75);
}
</style>
