<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import TunnelTeledeclarationAccordionItem from '@/components/TunnelTeledeclarationAccordionItem.vue'

/* Router */
const route = useRoute()

/* Stores */
const canteenStore = useStoreCanteen()
const teledeclarationStore = useStoreTeledeclaration()
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnostic } = storeToRefs(teledeclarationStore)

/* Accordions */
const activeAccordion = ref()
const accordions = computed(() => {
  const isGroupe = canteenInformations.value.isGroupe
  const isSimple = diagnostic.value.diagnosticType === "SIMPLE"
  return [
    {
      title: isGroupe ? "Informations du groupe" : "Informations de la cantine",
      to: { name: isGroupe ? 'GestionnaireCantineGroupeModifier' : 'GestionnaireCantineRestaurantModifier', query: { redirection: route.fullPath } },
      isCanteenFields: true,
      fieldsGroupName: isGroupe ? "informationsGroupe" : "informationsCantine"
    },
    {
      title: "Couverts annuels",
      to: { name: 'GestionnaireTunnelApproCouverts' },
      fieldsGroupName: "couverts"
    },
    {
      title: "Mode de saisie",
      to: { name: 'GestionnaireTunnelApproSaisie' },
      fieldsGroupName: "saisie"
    },
    {
      title: "EGalim",
      to: { name: 'GestionnaireTunnelApproEgalim' },
      fieldsGroupName: isSimple ? "egalimSimple" : "egalimComplete"
    },
    {
      title: "Origine France et UE",
      to: { name: 'GestionnaireTunnelApproOrigine' },
      fieldsGroupName: "origine"
    },
    {
      title: "« Local » et circuit court",
      to: { name: 'GestionnaireTunnelApproLocalCircuitCourt' },
      fieldsGroupName: "localCircuitCourt"
    }
  ]
})
</script>

<template>
  <h3 class="fr-h6">Récapitulatif des données d’approvisionnements saisies :</h3>
  <DsfrAccordionsGroup v-model="activeAccordion" class="fr-mb-4w">
    <TunnelTeledeclarationAccordionItem
      v-for="(accordion, index) in accordions"
      :key="accordion.title"
      :id="`accordion-${index}`"
      :accordion="accordion"
    />
  </DsfrAccordionsGroup>
</template>
