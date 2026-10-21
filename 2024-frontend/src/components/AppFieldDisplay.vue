<script setup>
import { computed } from 'vue'
import AppTooltipHover from '@/components/AppTooltipHover.vue'

const props = defineProps(['label', 'value', 'tooltip', 'error'])

/* Values are rendered as text (not HTML): they can contain user input (canteen name...) */
const valueLines = computed(() => {
  const values = Array.isArray(props.value) ? props.value : [props.value]
  const valueIsEmpty = values.length === 0 || values.every((value) => value === null || value === undefined || value === '')
  return valueIsEmpty ? ['Non renseigné'] : values
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
        <div>
          <template v-for="(value, index) in valueLines" :key="index">
            {{ value }}<template v-if="index < valueLines.length - 1"> ;<br/></template>
          </template>
        </div>
        <AppTooltipHover v-if="tooltip" :content="tooltip" class="fr-ml-1w fr-mt-n1v" />
      </div>
      <p v-if="hasError" class="fr-message fr-message--error">{{ errorMessage }}</p>
    </div>
  </div>
</template>
