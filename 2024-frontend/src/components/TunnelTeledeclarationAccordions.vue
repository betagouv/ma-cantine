<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreDiagnostic } from '@/stores/diagnostic'
import teledeclaration from '@/data/teledeclaration.json'
import CanteenDisplayInformations from '@/components/CanteenDisplayInformations.vue'

/* Router */
const router = useRouter()
const route = useRoute()

/* Stores */
const canteenStore = useStoreCanteen()
const diagnosticStore = useStoreDiagnostic()
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnosticCurrentCampaign } = storeToRefs(diagnosticStore)

/* Data */
const header = [
  { key: "name", label: "Champ" },
  { key: "value", label: "Valeur" },
]

const getPrettyDiagnosticValue = (field) => {
  const hasOptions = teledeclaration.fields[field]?.options?.length > 0
  const diagValue = diagnosticCurrentCampaign.value[field]
  const prettyValue = hasOptions ? teledeclaration.fields[field].options.find(option => option.value === diagValue).labelShort : diagValue
  return prettyValue || "Non renseigné"
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
  const isSimple = diagnosticCurrentCampaign.value.diagnosticType === "SIMPLE"
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
  <DsfrAccordionsGroup v-model="activeAccordion" class="fr-mb-4w">
    <DsfrAccordion
      v-for="(accordion, index) in accordions"
      :key="accordion.title"
      :id="`accordion-${index}`"
      :title="accordion.title"
    >
      <div class="ma-cantine--flex ma-cantine--flex-between fr-mb-2w">
        <p class="fr-mb-0 fr-text--bold">Récapitulatif des données saisies :</p>
        <DsfrButton label="Modifier les données" @click="goToStep(accordion.to)" icon="ri-pencil-line" secondary />
      </div>
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
        class="fr-mb-0 fr-table--no-scroll"
      />
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>
