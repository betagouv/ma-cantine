<script setup>
import { computed } from "vue"
import stringsService from "@/services/strings"
import teledeclarationFieldsService from "@/services/teledeclarationFields"
import GraphEgalim from "@/components/GraphEgalim.vue"
import AppSeparator from "@/components/AppSeparator.vue"

const props = defineProps(['diagnosticRecap'])

const approStats = computed(() => props.diagnosticRecap?.canteenDiagnosticApproStats)
const objectives = computed(() => props.diagnosticRecap?.notes)

/* Groups fields */
const franceFields = [
  "pourcentageViandesVolaillesFrance",
  "pourcentageProduitsDeLaMerFrance",
  "pourcentageCharcuterieFrance",
  "pourcentageFruitsEtLegumesFrance",
  "pourcentageProduitsLaitiersFrance",
  "pourcentageBoulangerieFrance",
  "pourcentageAutresFrance",
  "pourcentageBoissonsFrance",
]
const europeFields = [
  "pourcentageViandesVolaillesEurope",
  "pourcentageProduitsDeLaMerEurope",
  "pourcentageCharcuterieEurope",
  "pourcentageFruitsEtLegumesEurope",
  "pourcentageProduitsLaitiersEurope",
  "pourcentageBoulangerieEurope",
  "pourcentageAutresEurope",
  "pourcentageBoissonsEurope",
]
const localFields = [
  "pourcentageViandesVolaillesLocal",
  "pourcentageProduitsDeLaMerLocal",
  "pourcentageCharcuterieLocal",
  "pourcentageFruitsEtLegumesLocal",
  "pourcentageProduitsLaitiersLocal",
  "pourcentageBoulangerieLocal",
  "pourcentageAutresLocal",
  "pourcentageBoissonsLocal",
]
const circuitCourtFields = [
  "pourcentageViandesVolaillesCircuitCourt",
  "pourcentageProduitsDeLaMerCircuitCourt",
  "pourcentageCharcuterieCircuitCourt",
  "pourcentageFruitsEtLegumesCircuitCourt",
  "pourcentageProduitsLaitiersCircuitCourt",
  "pourcentageBoulangerieCircuitCourt",
  "pourcentageAutresCircuitCourt",
  "pourcentageBoissonsCircuitCourt",
]
const groups = [
  { title: "Origine France", total: "pourcentageFrance", fields: franceFields },
  { title: "Origine Europe (hors France)", total: "pourcentageEurope", fields: europeFields },
  { title: "« Local »", total: "pourcentageLocal", fields: localFields },
  { title: "Circuit court", total: "pourcentageCircuitCourt", fields: circuitCourtFields },
]

/* Display group if needed */
const hasValue = (statName) => {
  const value = approStats.value?.[statName]
  return value !== null && value !== undefined
}
const displayedGroups = computed(() => groups.filter((group) => hasValue(group.total)))

/* Get values */
const getLabel = (statName) => teledeclarationFieldsService.getField(statName.replace("pourcentage", "valeur")).label
const getResult = (statName) => hasValue(statName) ? stringsService.prettyPercent(approStats.value[statName]) : "Non renseigné"
</script>
<template>
  <GraphEgalim
    :egalim-percent="approStats.pourcentageEgalim"
    :bio-percent="approStats.pourcentageBio"
    :viandes-poissons-egalim-percent="approStats.pourcentageViandesVolaillesProduitsDeLaMerEgalim"
    :egalim-objective="objectives.egalimPercentObjective"
    :bio-objective="objectives.bioPercentObjective"
    :mention="`sur ${stringsService.prettyPercent(100)} du Total de vos achats`"
    :year="diagnosticRecap.year"
    :description-custom="`Pour le bilan ${diagnosticRecap.year}`"
  />
  <AppSeparator v-if="displayedGroups.length > 0" class="fr-mt-4w" />
  <template v-for="group in displayedGroups" :key="group.title">
    <div class="fr-mt-4w">
      <h3 class="fr-h6 fr-mb-2w">{{ group.title }}</h3>
      <ul class="ma-cantine--unstyled-list fr-grid-row">
        <li class="fr-col-12">
          <p class="fr-text--sm fr-mb-0">
            {{ getLabel(group.total) }} : <strong>{{ getResult(group.total) }}</strong>
          </p>
        </li>
        <li v-for="field in group.fields" :key="field" class="fr-col-12 fr-col-md-6">
          <p class="fr-text--sm fr-mb-0">
            {{ getLabel(field) }} : <strong>{{ getResult(field) }}</strong>
          </p>
        </li>
      </ul>
    </div>
  </template>
</template>
