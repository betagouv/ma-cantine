<script setup>
import { computed } from 'vue'
import AppRawHtml from '@/components/AppRawHtml.vue'

const props = defineProps(['label', 'value', 'tooltip', 'error'])

const valueFormatted = computed(() => {
  const isArray = Array.isArray(props.value)
  const value = isArray ? props.value?.join(' ; <br/>') : props.value
  const valueIsEmpty = value === null || value === undefined || value === ''
  return valueIsEmpty ? 'Non renseigné' : value
})

const hasError = computed(() => props.error && props.error.length > 0)
const errorMessage = computed(() => hasError.value ? props.error?.join(' ') : "")
</script>

<template>
  <div class="app-field-display fr-grid-row fr-grid-row--gutters fr-mb-1w">
    <div class="fr-col-12 fr-col-md-5">
      <p class="fr-mb-0 fr-text--bold">{{ label }} :</p>
    </div>
    <div class="fr-col-12 fr-col-md-7">
      <div class="ma-cantine--flex-start ma-cantine--flex-top fr-mb-1w">
        <AppRawHtml :html="valueFormatted" />
        <DsfrTooltip v-if="tooltip" :content="tooltip" />
      </div>
      <p v-if="hasError" class="fr-message fr-message--error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<style lang="scss">
.app-field-display {
  .fr-btn--tooltip {
    min-height: auto !important;
  }
}
</style>
