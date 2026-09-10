<script setup>
import { ref, computed, onMounted } from "vue"
import { storeToRefs } from "pinia"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import { formatNumber } from "@/utils.js"
import diagnosticsFieldsService from "@/services/diagnosticsFields.js"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

/* Stores */
const storePurchaseSummary = useStorePurchaseSummary()
const storeTeledeclaration = useStoreTeledeclaration()

/* Select */
const select = ref()
const fieldName = "diagnosticType"
const field = computed(() => diagnosticsFieldsService.getField(fieldName))
const isRequired = computed(() => field.value.required)
const label = computed(() => field.value.label)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(fieldName, storeTeledeclaration.diagnosticErrors))
const options = computed(() => {
  const newOptions = field.value.options || []
  const autoIndex = newOptions.findIndex(field => field.value === "AUTO")
  newOptions[autoIndex].disabled = !hasPurchaseTotal.value
  newOptions[autoIndex].hint = !hasPurchaseTotal.value ? "Aucun achat détecté" : `${formatNumber(purchaseSummary.value?.valeurTotale)}€ d'achats détectés dans votre suivi des achats`
  return newOptions
})

/* OSA */
const { purchaseSummary, hasPurchaseTotal } = storeToRefs(storePurchaseSummary)

/* Prefill */
const prefillSelect = () => { select.value = storeTeledeclaration.diagnostic[fieldName] || "SIMPLE" } // By defaut to SIMPLE to avoid error because it's not required in backend
onMounted(prefillSelect)

/* Change */
const selectRadio = () => {
  if (select.value === "AUTO") alert('TODO: Saisie auto')
  else storeTeledeclaration.setValue(fieldName, select.value)
}
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p>Plusieurs modes de saisie existent pour renseigner les données d’approvisionnements EGalim : simplifiée, détaillée et automatique.</p>
      <p>La saisie automatique est disponible uniquement si vous utilisez <AppLinkRouter :to="{ name: 'PurchasesHome' }" title="Outil de Suivi des Achats" /> de <em>ma cantine</em>.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Télédéclaration simplifiée ou détaillée : laquelle choisir ?">
        <a target="_blank" :href="documentation.teledeclarationType">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <DsfrRadioButtonSet
    v-model="select"
    :small="true"
    :required="isRequired"
    :legend="label"
    :options="options"
    @change="selectRadio"
    :error-message="errorMessage"
  />
</template>
