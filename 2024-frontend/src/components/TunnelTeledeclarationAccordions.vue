<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreDiagnostic } from '@/stores/diagnostic'
import teledeclaration from '@/data/teledeclaration.json'

/* Router */
const router = useRouter()

/* Stores */
const canteenStore = useStoreCanteen()
const diagnosticStore = useStoreDiagnostic()
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnosticCurrentCampaign } = storeToRefs(diagnosticStore)

/* Accordions */
const activeAccordion = ref()
const accordions = computed(() => {
  const isGroupe = canteenInformations.value.isGroupe
  const isSimple = diagnosticCurrentCampaign.value.diagnosticType === "SIMPLE"
  return [
    {
      title: isGroupe ? "Informations du groupe" : "Informations de la cantine",
      fields: isGroupe ? teledeclaration.groups.informationsGroupe : teledeclaration.groups.informationsCantine,
      to: { name: 'GestionnaireTunnelApproInformations' },
      isCanteenFields: true
    },
    {
      title: "Couverts annuels",
      fields: teledeclaration.groups.couverts,
      to: { name: 'GestionnaireTunnelApproCouverts' }
    },
    {
      title: "Mode de saisie",
      fields: teledeclaration.groups.saisie,
      to: { name: 'GestionnaireTunnelApproSaisie' }
    },
    {
      title: "EGalim",
      fields: isSimple ? teledeclaration.groups.egalimSimple : teledeclaration.groups.egalimDetaille,
      to: { name: 'GestionnaireTunnelApproEgalim' }
    },
    {
      title: "Origine France et UE",
      fields: teledeclaration.groups.origine,
      to: { name: 'GestionnaireTunnelApproOrigine' }
    },
    {
      title: "« Local » et circuit court",
      fields: teledeclaration.groups.localCircuitCourt,
      to: { name: 'GestionnaireTunnelApproLocalCircuitCourt' }
    }
  ]
})
const goToStep = (page) => router.push(page)
</script>

<template>
  <DsfrAccordionsGroup v-model="activeAccordion">
    <DsfrAccordion
      v-for="(accordion, index) in accordions"
      :key="accordion.title"
      :id="`accordion-${index}`"
      :title="accordion.title"
    >
      <div class="ma-cantine--flex ma-cantine--flex-between fr-mb-2w">
        <p class="fr-mb-0 fr-text--bold">Champs enregistrés :</p>
        <DsfrButton label="Modifier les données" @click="goToStep(accordion.to)" icon="ri-pencil-line" secondary />
      </div>
      <div v-for="field in accordion.fields" :key="field">
        <pre>{{ field }}</pre>
      </div>
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>
