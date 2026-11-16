<script setup>
const props = defineProps(["text", "mention", "inline"])
</script>

<template>
  <DsfrCallout class="tunnel-teledeclaration-callout">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div class="fr-col-12" :class="{ 'fr-col-md-10': props.inline }">
        <p class="fr-mb-0">{{ props.text }}</p>
        <p v-if="mention" class="fr-text--sm fr-text-mention--grey fr-mb-0">{{ props.mention }}</p>
      </div>
      <div class="fr-col-12" :class="{ 'fr-col-md-2': props.inline }">
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
