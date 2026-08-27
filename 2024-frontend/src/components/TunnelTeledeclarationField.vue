<script setup>
import { ref, computed, onMounted } from "vue"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary"
import { storeToRefs } from "pinia"
import diagnosticsFieldsService from "@/services/diagnosticsFields"

const props = defineProps(["name"])
const storeDiagnostic = useStoreDiagnostic()
const storePurchaseSummary = useStorePurchaseSummary()
const { diagnosticCurrentCampaign } = storeToRefs(storeDiagnostic)
const { purchaseSummary } = storeToRefs(storePurchaseSummary)
const data = computed(() => diagnosticsFieldsService.getField(props.name))
const field = ref()

/* Informations */
const isNumber = computed(() => data.value.type === "number")
const isRequired = computed(() => data.value.required)
const label = computed(() => data.value.label)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(props.name, storeDiagnostic.diagnosticCurrentCampaignErrors))
const hint = computed(() => {
  const enablePurchaseSummary = data.value.enablePurchaseSummary
  return enablePurchaseSummary ? `Vous avez ${purchaseSummary.value[diagnosticCurrentCampaign.value.year][props.name]}€ renseignés dans l'Outil de Suivi des Achats` : data.value.hint
})

/* Actions */
const fieldChange = () =>  storeDiagnostic.setDiagnosticCurrentCampaign(props.name, field.value)
const prefillField = () => field.value = storeDiagnostic.diagnosticCurrentCampaign[props.name]
onMounted(prefillField)
</script>
<template>
  <DsfrInputGroup v-if="isNumber" v-model="field" :label="label" :label-visible="true" :name="props.name" type="number" :required="isRequired" @change="fieldChange" :error-message="errorMessage" :hint="hint" />
  <pre v-else>{{ field }}</pre>
</template>
