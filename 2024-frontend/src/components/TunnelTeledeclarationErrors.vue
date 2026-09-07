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
const checkDiag = computedAsync(async () => await diagnosticServices.checkDiagnostic(canteenId.value, diagnosticCurrentCampaign.value.id), false)
const hasErrors = computed(() => checkDiag.value && !checkDiag.value?.isFilled)
const errors = computed(() => {
  if (!hasErrors.value) return []
  return Object.keys(checkDiag.value.errors)
})
const badge = computed(() => {
  if (!hasErrors.value) return false
  const count = errors.value.length
  const sentence = count > 1 ? 'erreurs détectées' : 'erreur détectée'
  return `${count} ${sentence}`
})
</script>
<template>
  <div v-if="hasErrors">
    <DsfrBadge :label="badge" type="error" />
    <ul>
      <li v-for="field in errors" :key="field" class="fr-text-default--error">
        <p class="fr-mb-0">
          erreur sur le champ <span class="ma-cantine--bold">« {{ field }} »</span>
        </p>
      </li>
    </ul>
  </div>
</template>
