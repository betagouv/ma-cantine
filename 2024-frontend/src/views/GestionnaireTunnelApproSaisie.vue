<script setup>
import { ref, computed, onMounted } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
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
const route = useRoute()

/* Select */
const select = ref()
const diagnosticTypeFieldName = "diagnosticType"
const generatedFromPurchasesFieldName = "generatedFromPurchases"
const field = computed(() => diagnosticsFieldsService.getField(diagnosticTypeFieldName))
const isRequired = computed(() => field.value.required)
const label = computed(() => field.value.label)
const errorMessage = computed(() => {
  const errors = diagnosticsFieldsService.getFieldError(diagnosticTypeFieldName, storeTeledeclaration.getDisplayedErrors(route.meta.slug))
  return errors ? errors.join('. ') : ''
})
const options = computed(() => {
  const newOptions = [...(field.value.options || [])]
  const autoIndex = newOptions.findIndex(field => field.value === "AUTO")
  newOptions[autoIndex] = getAutoOption(newOptions[autoIndex])
  return newOptions
})
const getAutoOption = (option) => {
  const autoOption = { ...option, disabled: !hasPurchaseTotal.value }
  autoOption.label = hasPurchaseTotal.value ? `Saisie automatique : vous utilisez l'Outil Suivi des Achats avec ${formatNumber(purchaseSummary.value?.valeurTotale)}€ d'achats détectés` : "Saisie automatique : vous n'utilisez pas l'Outil Suivi des Achats"
  autoOption.hint = hasPurchaseTotal.value ? "Tous les champs de la télédéclaration seront automatiquement renseignés." : undefined
  if (hasPurchaseTotal.value && hasPurchaseLocal.value) autoOption.hint += " Vous avez également des achats « locaux », un des champs de la catégorie n'est pas automatisable : « définition de local », vous devrez le renseigner manuellement pour finaliser votre télédéclaration."
  return autoOption
}

/* OSA */
const { purchaseSummary, hasPurchaseTotal } = storeToRefs(storePurchaseSummary)
const hasPurchaseLocal = computed(() => purchaseSummary.value?.valeurLocal > 0)

/* Prefill */
const prefillSelect = () => {
  const diagnostic = storeTeledeclaration.diagnostic
  select.value = diagnostic[generatedFromPurchasesFieldName] ? "AUTO" : diagnostic[diagnosticTypeFieldName]
}
onMounted(prefillSelect)

/* Change */
const selectRadio = () => {
  const isAuto = select.value === "AUTO"
  storeTeledeclaration.setSelectAutofill(isAuto)
  storeTeledeclaration.setValue(diagnosticTypeFieldName, isAuto ? "COMPLETE" : select.value)
  if (!isAuto) storeTeledeclaration.setValue(generatedFromPurchasesFieldName, false)
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
