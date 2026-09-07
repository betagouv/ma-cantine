<script setup>
import { computed } from 'vue'
import { computedAsync } from '@vueuse/core'
import { useStoreDiagnostic } from '@/stores/diagnostic'
import { storeToRefs } from 'pinia'
import diagnosticServices from '@/services/diagnostics'
import canteenServices from '@/services/canteens'

const diagnosticStore = useStoreDiagnostic()
const { diagnosticCurrentCampaign } = storeToRefs(diagnosticStore)
const canteenId = computed(() => diagnosticCurrentCampaign.value.canteenId)

/* Checks */
const checkCanteen = computedAsync(async () => await canteenServices.checkCanteen(canteenId.value), false)
const checkDiagnostic = computedAsync(async () => await diagnosticServices.checkDiagnostic(canteenId.value, diagnosticCurrentCampaign.value.id), false)

/* Errors */
const hasCanteenErrors = computed(() => checkCanteen.value && !checkCanteen.value?.isFilled)
const hasDiagnosticErrors = computed(() => checkDiagnostic.value && !checkDiagnostic.value?.isFilled)
const hasErrors = computed(() => hasCanteenErrors.value || hasDiagnosticErrors.value)

const errors = computed(() => {
  const canteenErrors = hasCanteenErrors.value ? Object.keys(checkCanteen.value.errors) : []
  const diagnosticErrors = hasDiagnosticErrors.value ? Object.keys(checkDiagnostic.value.errors) : []
  return [...canteenErrors, ...diagnosticErrors]
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
