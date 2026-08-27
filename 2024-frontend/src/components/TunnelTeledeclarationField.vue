<script setup>
import { ref, computed, onMounted } from "vue"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary"
import { storeToRefs } from "pinia"
import { formatNumber } from "@/utils.js"
import diagnosticsFieldsService from "@/services/diagnosticsFields"


/* Stores */
const props = defineProps(["name"])
const storeDiagnostic = useStoreDiagnostic()
const storePurchaseSummary = useStorePurchaseSummary()
const { diagnosticCurrentCampaign } = storeToRefs(storeDiagnostic)
const { purchaseSummary } = storeToRefs(storePurchaseSummary)

/* Informations */
const field = ref()
const data = computed(() => diagnosticsFieldsService.getField(props.name))
const isNumber = computed(() => data.value.type === "number")
const isRequired = computed(() => data.value.required)
const label = computed(() => data.value.label)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(props.name, storeDiagnostic.diagnosticCurrentCampaignErrors))
const hint = computed(() => {
  const enablePurchaseSummary = data.value.enablePurchaseSummary
  const hasPurchaseSummary = storePurchaseSummary.hasPurchaseTotal(diagnosticCurrentCampaign.value.year)
  return enablePurchaseSummary && hasPurchaseSummary ? getPurchaseSummaryHint(props.name) : data.value.hint
})

const getPurchaseSummaryHint = (fieldName) => {
  const fieldValue = purchaseSummary.value[diagnosticCurrentCampaign.value.year][fieldName]
  if (!fieldValue) return "0€ dans l'Outil de Suivi des Achats"
  else if (fieldValue === 1) return "1€ renseigné dans l'Outil de Suivi des Achats"
  else return `${formatNumber(fieldValue)}€ sont renseignés dans l'Outil de Suivi des Achats`
}

/* Actions */
const fieldChange = () =>  storeDiagnostic.setDiagnosticCurrentCampaign(props.name, field.value)
const prefillField = () => field.value = storeDiagnostic.diagnosticCurrentCampaign[props.name]
onMounted(prefillField)
</script>
<template>
  <DsfrInputGroup v-if="isNumber" v-model="field" :label="label" :label-visible="true" :name="props.name" type="number" :required="isRequired" @change="fieldChange" :error-message="errorMessage" :hint="hint" />
  <pre v-else>{{ field }}</pre>
</template>
