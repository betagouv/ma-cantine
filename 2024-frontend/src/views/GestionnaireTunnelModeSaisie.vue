<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import { useStoreDiagnostic } from "@/stores/diagnostic.js"
import { formatNumber } from "@/utils.js"
import diagnosticsFieldsService from "@/services/diagnosticsFields.js"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

/* Stores */
const route = useRoute()
const storePurchaseSummary = useStorePurchaseSummary()
const storeDiagnostic = useStoreDiagnostic()

/* Fields */
const pageName = route.name
const fields = computed(() => diagnosticsFieldsService.getPageFields(pageName))

/* Customize select option */
const options = computed(() => {
  const defaultOptions = diagnosticsFieldsService.getField(fields.value[0]).options || []
  const autoIndex = defaultOptions.findIndex(field => field.value === "AUTO")
  defaultOptions[autoIndex].disabled = !hasPurchaseSummary.value
  defaultOptions[autoIndex].hint = !hasPurchaseSummary.value ? "Aucun achat détecté" : `${formatNumber(purchaseSummary.value[diagYear].valeurTotale)}€ d'achats détectés dans votre suivi des achats`
  return defaultOptions
})

/* Saisie automatique */
const diagYear = storeDiagnostic.diagnosticCurrentCampaign.year
const { purchaseSummary } = storeToRefs(storePurchaseSummary)
const hasPurchaseSummary = computed(() => storePurchaseSummary.hasPurchaseTotal(diagYear))
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
  <TunnelTeledeclarationField v-for="field in fields" :key="field" :name="field" :custom-select-options="options" />
</template>
