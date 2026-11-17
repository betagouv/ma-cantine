<script setup>
import TunnelTeledeclarationLockedInput from "@/components/TunnelTeledeclarationLockedInput.vue"
import AppTooltipHover from "@/components/AppTooltipHover.vue"

defineProps(["text", "mention", "value", "errorMessage", "tooltip"])
</script>

<template>
  <DsfrCallout class="tunnel-teledeclaration-callout-field">
    <slot name="introduction" />
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-7">
        <p class="fr-mb-0">{{ text }}</p>
        <p v-if="mention" class="fr-text--sm fr-text-mention--grey fr-mb-0">{{ mention }}</p>
      </div>
      <div class="fr-col-12 fr-col-md-5 ma-cantine--flex-between ma-cantine--flex-top">
        <div class="ma-cantine--flex-grow">
          <TunnelTeledeclarationLockedInput :value="value" :label="text" :error-message="errorMessage" />
        </div>
        <AppTooltipHover v-if="tooltip" :content="tooltip" class="fr-ml-1w fr-mt-3v ma-cantine--flex-shrink-0" />
      </div>
    </div>
  </DsfrCallout>
</template>

<style lang="scss">
.tunnel-teledeclaration-callout-field {
  background-image: linear-gradient(0deg, var(--border-default-blue-france), var(--border-default-blue-france)) !important;
  background-size: 100% 0.25rem !important;
  background-position: 0 0 !important;
}
</style>
