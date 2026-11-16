<script setup>
const props = defineProps(["text", "mention"])
</script>

<template>
  <DsfrCallout class="tunnel-teledeclaration-callout">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-10">
        <p class="fr-mb-0">{{ props.text }}</p>
        <p v-if="mention" class="fr-text--sm fr-text-mention--grey fr-mb-0">{{ props.mention }}</p>
      </div>
      <div class="fr-col-12 fr-col-md-2">
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
