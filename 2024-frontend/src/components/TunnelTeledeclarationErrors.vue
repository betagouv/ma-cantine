<script setup>
import { computed } from 'vue'
import { computedAsync } from '@vueuse/core'
import { useStoreDiagnostic } from '@/stores/diagnostic'
import { storeToRefs } from 'pinia'
import diagnosticServices from '@/services/diagnostics'

const diagnosticStore = useStoreDiagnostic()
const { diagnosticCurrentCampaign } = storeToRefs(diagnosticStore)
const canteenId = computed(() => diagnosticCurrentCampaign.value.canteenId)

/* Errors */
const check = computedAsync(async () => await diagnosticServices.checkDiagnostic(canteenId.value, diagnosticCurrentCampaign.value.id), false)
const hasErrors = computed(() => !check.value.isFilled )
const errors = computed(() => {
  if (!hasErrors.value || !check.value ) return []
  const keys = Object.keys(check.value.errors)
  const values = Object.values(check.value.errors)
  const errors = []
  for (let i = 0; i < keys.length; i++) {
    errors.push({
      field: keys[i],
      messages: values[i].join('. ')
    })
  }
  return errors
})
const badge = computed(() => {
  if (!hasErrors.value || !check.value) return false
  const count = errors.value.length
  const sentence = count > 1 ? 'erreurs détectées' : 'erreur détectée'
  return `${count} ${sentence}`
})
</script>
<template>
  <div v-if="hasErrors" class="fr-mb-4w">
    <DsfrBadge :label="badge" type="error" />
    <ul>
      <li v-for="error in errors" :key="error.field" class="fr-text-default--error">
        <p class="fr-mb-0">
          <span class="ma-cantine--bold">{{ error.field }} :</span>
          {{ error.messages }}
        </p>
      </li>
    </ul>
  </div>
</template>
