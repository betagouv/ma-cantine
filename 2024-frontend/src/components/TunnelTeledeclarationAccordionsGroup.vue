<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import teledeclaration from '@/data/teledeclaration.json'
import TunnelTeledeclarationAccordionItem from '@/components/TunnelTeledeclarationAccordionItem.vue'
import AppSeparator from '@/components/AppSeparator.vue'

/* Router */
const route = useRoute()

/* Stores */
const canteenStore = useStoreCanteen()
const teledeclarationStore = useStoreTeledeclaration()
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnostic } = storeToRefs(teledeclarationStore)

/* Data */
const getPrettyDiagnosticValue = (field) => {
  const hasOptions = teledeclaration.fields[field]?.options?.length > 0
  const diagValue = diagnostic.value[field]
  const prettyValue = hasOptions ? teledeclaration.fields[field].options.find(option => option.value === diagValue).labelShort : diagValue
  return prettyValue !== null ? prettyValue : "Non renseigné"
}

const getFields = (fields, source) => {
  return fields.map(field => {
    const isCanteen = source === "canteen"
    const name = isCanteen ? field : teledeclaration.fields[field].label
    const value = isCanteen ? canteenInformations.value[field] : getPrettyDiagnosticValue(field)
    return {
      name,
      value,
    }
  })
}

/* Accordions */
const activeAccordion = ref()
const accordions = computed(() => {
  const isGroupe = canteenInformations.value.isGroupe
  const isSimple = diagnostic.value.diagnosticType === "SIMPLE"
  return [
    {
      title: isGroupe ? "Informations du groupe" : "Informations de la cantine",
      rows: getFields(isGroupe ? teledeclaration.groups.informationsGroupe : teledeclaration.groups.informationsCantine, "canteen"),
      to: { name: isGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier', query: { redirection: route.fullPath } },
      isCanteenFields: true,
      fieldsGroupName: isGroupe ? "informationsGroupe" : "informationsCantine"
    },
    {
      title: "Couverts annuels",
      rows: getFields(teledeclaration.groups.couverts, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproCouverts' },
      fieldsGroupName: "couverts"
    },
    {
      title: "Mode de saisie",
      rows: getFields(teledeclaration.groups.saisie, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproSaisie' },
      fieldsGroupName: "saisie"
    },
    {
      title: "EGalim",
      rows: getFields(isSimple ? teledeclaration.groups.egalimSimple : teledeclaration.groups.egalimDetaille, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproEgalim' },
      fieldsGroupName: isSimple ? "egalimSimple" : "egalimDetaille"
    },
    {
      title: "Origine France et UE",
      rows: getFields(teledeclaration.groups.origine, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproOrigine' },
      fieldsGroupName: "origine"
    },
    {
      title: "« Local » et circuit court",
      rows: getFields(teledeclaration.groups.localCircuitCourt, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproLocalCircuitCourt' },
      fieldsGroupName: "localCircuitCourt"
    }
  ]
})
</script>

<template>
  <AppSeparator class="fr-mb-3w" />
  <p class="fr-text--bold fr-text--sm ma-cantine--text-uppercase">Récapitulatif des données saisies :</p>
  <DsfrAccordionsGroup v-model="activeAccordion" class="fr-mb-4w">
    <TunnelTeledeclarationAccordionItem
      v-for="(accordion, index) in accordions"
      :key="accordion.title"
      :id="`accordion-${index}`"
      :accordion="accordion"
    />
  </DsfrAccordionsGroup>
</template>
