<script setup>
import { computed } from "vue"

const props = defineProps(["text", "mention", "colSizes"])

const cols = computed(() => ({
  left: `fr-col-12 fr-col-md-${props.colSizes?.left || 6}`,
  right: `fr-col-12 fr-col-md-${props.colSizes?.right || 6}`,
}))
</script>

<template>
  <DsfrCallout class="tunnel-teledeclaration-callout">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div :class="cols.left">
        <p class="fr-mb-0">{{ text }}</p>
        <p v-if="mention" class="fr-text--sm fr-text-mention--grey fr-mb-0">{{ mention }}</p>
      </div>
      <div :class="cols.right">
        <slot />
      </div>
    </div>
  </DsfrCallout>
</template>

<style lang="scss">
.tunnel-teledeclaration-callout {
  background-image: linear-gradient(0deg, var(--border-default-blue-france), var(--border-default-blue-france));
  background-size: 100% 0.25rem;
  background-position: 0 0;
}
</style>
