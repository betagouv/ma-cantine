<script setup>
import { ref, computed, onMounted } from "vue"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary"
import { storeToRefs } from "pinia"
import { formatNumber } from "@/utils.js"
import diagnosticsFieldsService from "@/services/diagnosticsFields"
import documentation from "@/data/documentation.json"

/* Stores */
const props = defineProps(["name", "size"])
const storeDiagnostic = useStoreDiagnostic()
const storePurchaseSummary = useStorePurchaseSummary()
const { diagnosticCurrentCampaign } = storeToRefs(storeDiagnostic)
const { purchaseSummary } = storeToRefs(storePurchaseSummary)

/* Informations */
const field = ref()
const data = computed(() => diagnosticsFieldsService.getField(props.name))
const isNumber = computed(() => data.value?.type === "number")
const isSelect = computed(() => data.value?.type === "select")
const isRequired = computed(() => data.value.required)
const label = computed(() => data.value.label)
const tooltip = computed(() => data.value.tooltip)
const isRelated = computed(() => data.value?.isRelatedField)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(props.name, storeDiagnostic.diagnosticCurrentCampaignErrors))
const hint = computed(() => {
  const enablePurchaseSummary = data.value.enablePurchaseSummary
  const hasPurchaseSummary = storePurchaseSummary.hasPurchaseTotal(diagnosticCurrentCampaign.value.year)
  return enablePurchaseSummary && hasPurchaseSummary ? getPurchaseSummaryHint(props.name) : data.value.hint
})
const img = computed(() => data.value.img)
const imgAlt = computed(() => data.value.imgAlt)
const modale = computed(() => data.value.modaleDocLink )
const opened = ref(false)
const options = computed(() => data.value.options)

const getPurchaseSummaryHint = (fieldName) => {
  const fieldValue = purchaseSummary.value[diagnosticCurrentCampaign.value.year][fieldName]
  if (!fieldValue) return "0€ dans l'Outil de Suivi des Achats"
  else if (fieldValue === 1) return "1€ renseigné dans l'Outil de Suivi des Achats"
  else return `${formatNumber(fieldValue)}€ sont renseignés dans l'Outil de Suivi des Achats`
}

/* Style */
const displayHalf = computed(() => props.size === "half")
const displayFull = computed(() => !props.size || props.size === "full")
const displayInline = computed(() => props.size === "inline")

/* Actions */
const fieldChange = () =>  storeDiagnostic.setDiagnosticCurrentCampaign(props.name, field.value)
const prefillField = () => field.value = storeDiagnostic.diagnosticCurrentCampaign[props.name]
onMounted(prefillField)
</script>
<template>
  <div class="fr-grid-row fr-mb-2w" :class="{ 'fr-col-6' : displayInline }">
    <div class="fr-grid-row" :class="{ 'fr-col-12': displayFull || displayInline, 'fr-col-7': displayHalf }">
      <div v-if="isRelated" class="tunnel-teledeclaration-field__related fr-col-1"></div>
      <div class="tunnel-teledeclaration-field__input" :class="{ 'fr-col-11': isRelated, 'fr-col-12': !isRelated }">
        <DsfrInputGroup v-if="isNumber" v-model="field" :label="label" :label-visible="true" :name="props.name" type="number" :required="isRequired" @change="fieldChange" :error-message="errorMessage" :hint="hint" />
        <DsfrSelect v-if="isSelect" v-model="field" :label="label" :label-visible="true" :name="props.name" :required="isRequired" :options="options" @change="fieldChange" :error-message="errorMessage" :hint="hint" />
      </div>
    </div>
    <div v-if="displayHalf" class="fr-col-5 fr-pl-1v fr-grid-row fr-grid-row--bottom">
      <div class="fr-col-1 fr-pb-1v">
        <DsfrTooltip v-if="tooltip" :content="tooltip" title="Infobulle" />
        <button v-else-if="modale" class="fr-btn--tooltip" @click="opened = true" title="En savoir plus">
          <VIcon name="ri-question-line" />
        </button>
      </div>
      <div class="fr-col-1"></div>
      <div class="fr-col-10">
        <img v-if="img" :src="img" :alt="imgAlt" class="tunnel-teledeclaration-field__img" />
      </div>
    </div>
  </div>
  <DsfrModal :opened="opened" class="fr-modal--opened" @close="opened = false" size="xl">
    <template #default>
      <iframe
        title="En savoir plus"
        :src="`${documentation[data.modaleDocLink]}/reader/compact/`"
        class="ma-cantine--modal-iframe"
        frameborder="0"
      ></iframe>
    </template>
  </DsfrModal>
</template>

<style scoped lang="scss">
.tunnel-teledeclaration-field {

  &__related {
    position: relative;
    overflow: hidden;

    &::before {
      content: "";
      position: absolute;
      left: 10%;
      bottom: 1.25rem;
      width: 1px;
      height: 100%;
      background-color: var(--border-plain-grey);
    }

    &::after {
      content: "";
      position: absolute;
      left: 10%;
      bottom: 1.25rem;
      height: 1px;
      width: 80%;
      background-color: var(--border-plain-grey);
    }
  }

  &__img {
    width: auto;
    height: 3rem;
    object-fit: contain;
    object-position: center left;
  }
}
</style>
