<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import teledeclaration from '@/data/teledeclaration.json'
import CanteenDisplayInformations from '@/components/CanteenDisplayInformations.vue'
import AppSeparator from '@/components/AppSeparator.vue'

/* Router */
const router = useRouter()
const route = useRoute()

/* Stores */
const canteenStore = useStoreCanteen()
const teledeclarationStore = useStoreTeledeclaration()
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnostic } = storeToRefs(teledeclarationStore)

/* Data */
const header = [
  { key: "name", label: "Champ" },
  { key: "value", label: "Valeur" },
]

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
      isCanteenFields: true
    },
    {
      title: "Couverts annuels",
      rows: getFields(teledeclaration.groups.couverts, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproCouverts' }
    },
    {
      title: "Mode de saisie",
      rows: getFields(teledeclaration.groups.saisie, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproSaisie' }
    },
    {
      title: "EGalim",
      rows: getFields(isSimple ? teledeclaration.groups.egalimSimple : teledeclaration.groups.egalimDetaille, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproEgalim' }
    },
    {
      title: "Origine France et UE",
      rows: getFields(teledeclaration.groups.origine, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproOrigine' }
    },
    {
      title: "« Local » et circuit court",
      rows: getFields(teledeclaration.groups.localCircuitCourt, "diagnostic"),
      to: { name: 'GestionnaireTunnelApproLocalCircuitCourt' }
    }
  ]
})
const goToStep = (page) => router.push(page)
</script>

<template>
  <AppSeparator class="fr-mb-3w" />
  <p class="fr-text--bold fr-text--sm ma-cantine--text-uppercase">Récapitulatif des données saisies :</p>
  <DsfrAccordionsGroup v-model="activeAccordion" class="fr-mb-4w">
    <DsfrAccordion
      v-for="(accordion, index) in accordions"
      :key="accordion.title"
      :id="`accordion-${index}`"
      :title="accordion.title"
    >
      <CanteenDisplayInformations
        v-if="index === 0"
        :canteenInformation="canteenInformations"
        :canteenIsGroupe="canteenInformations.isGroupe"
      />
      <DsfrDataTable
        v-else
        title="Données enregistrées"
        no-caption
        :headersRow="header"
        :rows="accordion.rows"
        :no-scroll="true"
        class="fr-mb-2w fr-mt-0"
      />
      <DsfrButton label="Modifier ces données" @click="goToStep(accordion.to)" icon="ri-pencil-line" secondary size="sm" />
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>
