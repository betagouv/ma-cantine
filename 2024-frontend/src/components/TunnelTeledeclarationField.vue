<script setup>
import { ref, computed, onMounted } from "vue"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import diagnosticsFieldsService from "@/services/diagnosticsFields"

const props = defineProps(["name", "customSelectOptions"])
const storeDiagnostic = useStoreDiagnostic()
const data = computed(() => diagnosticsFieldsService.getField(props.name))
const field = ref()

/* Informations */
const type = computed(() => data.value.type)
const isRequired = computed(() => data.value.required)
const label = computed(() => data.value.label)
const options = computed(() => props.customSelectOptions || data.value.options)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(props.name, storeDiagnostic.diagnosticCurrentCampaignErrors))

/* Actions */
const fieldChange = () => { storeDiagnostic.setDiagnosticCurrentCampaign(props.name, field.value) }
const prefillField = () => { field.value = storeDiagnostic.diagnosticCurrentCampaign[props.name] }
onMounted(prefillField)
</script>
<template>
  <DsfrInputGroup
    v-if="type === 'number'"
    type="number"
    v-model="field"
    :label="label"
    :label-visible="true"
    :name="props.name"
    :required="isRequired"
    @change="fieldChange"
    :error-message="errorMessage"
  />
  <DsfrRadioButtonSet
    v-else-if="type === 'radioRiche'"
    v-model="field"
    :small="true"
    :required="isRequired"
    :legend="label"
    :options="options"
    @change="fieldChange"
    :error-message="errorMessage"
  />
  <pre v-else>{{ data }}</pre>
</template>
