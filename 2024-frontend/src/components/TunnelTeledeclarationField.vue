<script setup>
import { ref, computed, onMounted } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary"
import IconLink from "@/components/IconLink.vue"
import AppSeparator from "@/components/AppSeparator.vue"
import AppTooltipHover from "@/components/AppTooltipHover.vue"
import TunnelTeledeclarationAutofill from "@/components/TunnelTeledeclarationAutofill.vue"
import diagnosticsFieldsService from "@/services/diagnosticsFields"

/* Stores */
const props = defineProps(["name"])
const emit = defineEmits(["change"])
const storeTeledeclaration = useStoreTeledeclaration()
const storePurchaseSummary = useStorePurchaseSummary()
const { purchaseSummary, hasPurchaseTotal } = storeToRefs(storePurchaseSummary)
const route = useRoute()

/* Informations */
const field = ref()
const data = computed(() => diagnosticsFieldsService.getField(props.name))
const isNumber = computed(() => data.value?.type === "number")
const isSelect = computed(() => data.value?.type === "select")
const diagnosticType = computed(() => storeTeledeclaration.diagnostic?.diagnosticType)
const isRequired = computed(() => data.value.requiredByType ? data.value.requiredByType[diagnosticType.value] : data.value.required)
const label = computed(() => data.value.label)
const tooltip = computed(() => data.value.tooltip)
const isRelatedVertical = computed(() => data.value?.isRelatedField === "vertical")
const isRelatedHorizontal = computed(() => data.value?.isRelatedField === "horizontal")
const placeholder = computed(() => isRequired.value ? undefined : data.value?.placeholder)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(props.name, storeTeledeclaration.getDisplayedErrors(route.meta.slug)))
const hint = computed(() => data.value.hint)
const options = computed(() => data.value.options)

/* OSA */
const isAutofill = computed(() => data.value?.autofill === true)
const displayAutofill = computed(() => hasPurchaseTotal.value && isAutofill.value)
const valueBeforeAutofill = ref()

/* Related vertical fields only display the hint */
const displayedLabel = computed(() => isRelatedVertical.value ? "" : label.value)

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
const prefillField = () => {
  field.value = storeTeledeclaration.diagnostic[props.name]
  valueBeforeAutofill.value = field.value
}
onMounted(prefillField)

/* Autofill */
const fillField = (amount) => {
  valueBeforeAutofill.value = field.value
  field.value = amount
  fieldChange()
}
const resetField = () => {
  const previousEqualsAutofill = Number(valueBeforeAutofill.value) === purchaseSummary.value?.[props.name]
  const emptyValue = isRequired.value ? 0 : null
  field.value = previousEqualsAutofill ? emptyValue : valueBeforeAutofill.value
  fieldChange()
}
</script>
<template>
  <div class="fr-grid-row fr-col-12 fr-mb-2w">
    <IconLink v-if="isRelatedVertical" class="fr-col-1" bottom="1.25rem" />
    <div v-if="isRelatedHorizontal" class="fr-col-2 fr-pr-3w ma-cantine--flex-start">
      <AppSeparator class="fr-m-0" />
    </div>
    <div class="fr-col">
      <DsfrInputGroup v-if="isNumber" v-model="field" :label="displayedLabel" :label-visible="true" :name="props.name" type="number" :required="isRequired" @change="fieldChange" :error-message="errorMessage" :hint="hint" :placeholder="placeholder" min="0" :wrapper-class="{ 'tunnel-teledeclaration-field__autofill-group': displayAutofill }">
        <template #before-input>
          <TunnelTeledeclarationAutofill v-if="displayAutofill" :name="props.name" :value="field" @fill="fillField" @reset="resetField" class="tunnel-teledeclaration-field__container-tag" />
        </template>
      </DsfrInputGroup>
      <DsfrSelect v-if="isSelect" v-model="field" :label="label" :label-visible="true" :name="props.name" :required="isRequired" :options="options" @update:modelValue="fieldChange" :error-message="errorMessage" :hint="hint"/>
    </div>
    <div v-if="tooltip" class="tunnel-teledeclaration-field__tooltip fr-pl-1w fr-pb-1v">
      <AppTooltipHover :content="tooltip" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.tunnel-teledeclaration-field {

  &__tooltip {
    align-self: flex-end;
  }

  &__autofill-group {
    display: grid;
    grid-template-columns: 1fr auto;
    grid-template-areas:
      "label label"
      "input osa"
      "messages messages";

    :deep(.fr-label) {
      grid-area: label;
    }

    :deep(input.fr-input) {
      grid-area: input;
      border-top-right-radius: 0;
    }

    :deep(.fr-messages-group) {
      grid-area: messages;
    }
  }

  &__container-tag {
    grid-area: osa;
  }
}
</style>
