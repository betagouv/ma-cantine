<script setup>
import { ref, computed, onMounted } from "vue"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import IconLink from "@/components/IconLink.vue"
import diagnosticsFieldsService from "@/services/diagnosticsFields"

/* Stores */
const props = defineProps(["name"])
const emit = defineEmits(["change"])
const storeTeledeclaration = useStoreTeledeclaration()

/* Informations */
const field = ref()
const data = computed(() => diagnosticsFieldsService.getField(props.name))
const isNumber = computed(() => data.value?.type === "number")
const isSelect = computed(() => data.value?.type === "select")
const isRequired = computed(() => data.value.required)
const label = computed(() => data.value.label)
const tooltip = computed(() => data.value.tooltip)
const isRelated = computed(() => data.value?.isRelatedField)
const placeholder = computed(() => data.value?.placeholder)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(props.name, storeTeledeclaration.diagnosticErrors))
const hint = computed(() => data.value.hint)
const options = computed(() => data.value.options)

/* Actions */
const cleanValue = (value) => {
  if (value === "") return null
  if (value < 0) return 0
  return value
}

const fieldChange = () =>  {
  field.value = cleanValue(field.value)
  storeTeledeclaration.setValue(props.name, field.value)
  emit("change", field.value)
}
const prefillField = () => field.value = storeTeledeclaration.diagnostic[props.name]
onMounted(prefillField)
</script>
<template>
  <div class="fr-grid-row fr-col-12 fr-mb-2w">
    <IconLink v-if="isRelated" class="fr-col-1" bottom="1.25rem" />
    <div class="fr-col">
      <DsfrInputGroup v-if="isNumber" v-model="field" :label="label" :label-visible="true" :name="props.name" type="number" :required="isRequired" @change="fieldChange" :error-message="errorMessage" :hint="hint" :placeholder="placeholder" min="0" />
      <DsfrSelect v-if="isSelect" v-model="field" :label="label" :label-visible="true" :name="props.name" :required="isRequired" :options="options" @update:modelValue="fieldChange" :error-message="errorMessage" :hint="hint"/>
    </div>
    <div v-if="tooltip" class="tunnel-teledeclaration-field__tooltip fr-pl-1w fr-pb-1v">
      <DsfrTooltip :content="tooltip" title="Infobulle" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.tunnel-teledeclaration-field {

  &__tooltip {
    align-self: flex-end;
  }
}
</style>
