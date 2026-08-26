<script setup>
import { ref, computed, onMounted } from "vue"
import { storeToRefs } from "pinia"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import { useStoreDiagnostic } from "@/stores/diagnostic.js"
import { formatNumber } from "@/utils.js"
import diagnosticsFieldsService from "@/services/diagnosticsFields.js"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

/* Stores */
const storePurchaseSummary = useStorePurchaseSummary()
const storeDiagnostic = useStoreDiagnostic()

/* Select */
const select = ref()
const fieldName = "diagnosticType"
const field = computed(() => diagnosticsFieldsService.getField(fieldName))
const isRequired = computed(() => field.value.required)
const label = computed(() => field.value.label)
const errorMessage = computed(() => diagnosticsFieldsService.getFieldError(fieldName, storeDiagnostic.diagnosticCurrentCampaignErrors))
const options = computed(() => {
  const newOptions = field.value.options || []
  const autoIndex = newOptions.findIndex(field => field.value === "AUTO")
  newOptions[autoIndex].disabled = !hasPurchaseSummary.value
  newOptions[autoIndex].hint = !hasPurchaseSummary.value ? "Aucun achat détecté" : `${formatNumber(purchaseSummary.value[diagYear].valeurTotale)}€ d'achats détectés dans votre suivi des achats`
  return newOptions
})

/* OSA */
const diagYear = storeDiagnostic.diagnosticCurrentCampaign.year
const { purchaseSummary } = storeToRefs(storePurchaseSummary)
const hasPurchaseSummary = computed(() => storePurchaseSummary.hasPurchaseTotal(diagYear))

/* Prefill */
const prefillSelect = () => { select.value = storeDiagnostic.diagnosticCurrentCampaign[fieldName] || "SIMPLE" } // By defaut to SIMPLE to avoid error because it's not required in backend
onMounted(prefillSelect)

/* Change */
const selectRadio = () => {
  if (select.value === "AUTO") alert('TODO: Saisie auto')
  else storeDiagnostic.setDiagnosticCurrentCampaign(fieldName, select.value)
}
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Choisissez votre mode de saisie</h2>
      <p>Deux formats existent pour les modes de saisie des données d’approvisionnements EGalim, un troisième est disponible uniquement si vous utilisez <AppLinkRouter :to="{ name: 'PurchasesHome' }" title="Outil de Suivi des Achats" /> de <em>ma cantine</em>.</p>
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
