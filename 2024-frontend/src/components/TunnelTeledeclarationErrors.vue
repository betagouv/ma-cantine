<script setup>
import { computed } from 'vue'
import { computedAsync } from '@vueuse/core'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import { storeToRefs } from 'pinia'
import diagnosticServices from '@/services/diagnostics'
import canteenServices from '@/services/canteens'
import AppErrorList from '@/components/AppErrorList.vue'

const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)
const canteenId = computed(() => diagnostic.value.canteenId)

/* Checks */
const checkCanteen = computedAsync(async () => await canteenServices.checkCanteen(canteenId.value), false)
const checkDiagnostic = computedAsync(async () => await diagnosticServices.checkDiagnostic(canteenId.value, diagnostic.value.id), false)

/* Errors */
const hasCanteenErrors = computed(() => checkCanteen.value && !checkCanteen.value?.isFilled)
const hasDiagnosticErrors = computed(() => checkDiagnostic.value && !checkDiagnostic.value?.isFilled)
const hasErrors = computed(() => hasCanteenErrors.value || hasDiagnosticErrors.value)

const errors = computed(() => {
  const canteenErrors = hasCanteenErrors.value ? Object.keys(checkCanteen.value.errors) : []
  const diagnosticErrors = hasDiagnosticErrors.value ? Object.keys(checkDiagnostic.value.errors) : []
  return [...canteenErrors, ...diagnosticErrors]
})
</script>
<template>
  <AppErrorList v-if="hasErrors" :errors="errors" />
</template>
