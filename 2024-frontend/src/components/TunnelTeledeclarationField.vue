<script setup>
import { ref, computed, onMounted } from "vue"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import diagnosticsFieldsService from "@/services/diagnosticsFields"

const props = defineProps(["name"])
const storeDiagnostic = useStoreDiagnostic()
const data = computed(() => diagnosticsFieldsService.getField(props.name))
const field = ref()

/* Informations */
const type = computed(() => data.value.type)
const isRequired = computed(() => data.value.required)
const label = computed(() => data.value.label)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(props.name, storeDiagnostic.diagnosticCurrentCampaignErrors))

/* Actions */
const fieldChange = () => {
  storeDiagnostic.setDiagnosticCurrentCampaign(props.name, field.value)
}
const prefillField = () => {
  field.value = storeDiagnostic.diagnosticCurrentCampaign[props.name]
}
onMounted(prefillField)
</script>
<template>
  <DsfrInputGroup v-if="type === 'number'" v-model="field" :label="label" :label-visible="true" :name="props.name" type="number" :required="isRequired" @change="fieldChange" :error-message="errorMessage" />
  <pre v-else>{{ data }}</pre>
</template>
