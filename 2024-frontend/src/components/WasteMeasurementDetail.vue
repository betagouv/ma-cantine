<script setup>
import { formatNumber } from "@/utils"

const props = defineProps(["measurement"])

const detailedFields = [
  {
    key: "totalMass",
    label: "Masse totale de gaspillage relevée sur la période de mesure",
  },
  {
    key: "daysInPeriod",
    label: "Période de mesure de mon gaspillage alimentaire",
    unit: "jours",
  },
  {
    label: "Nombre de couverts sur la période",
    unit: "couverts",
    key: "mealCount",
  },
  {
    key: "totalYearlyWasteEstimation",
    label: "Masse totale de gaspillage sur l'année",
    unit: "kg",
    tooltip:
      "Calculé en prenant le gaspillage par repas pour la période, multiplié par le nombre de couverts par année pour l'établissement",
  },
  {
    heading: "Excédents de préparation",
  },
  {
    label: "Gaspillage total",
    key: "preparationTotalMass",
  },
  {
    label: "Gaspillage de denrées comestibles",
    key: "preparationEdibleMass",
  },
  {
    label: "Gaspillage de denrées non comestibles",
    key: "preparationInedibleMass",
  },
  {
    heading: "Denrées présentées aux convives mais non servies",
  },
  {
    label: "Gaspillage total",
    key: "unservedTotalMass",
  },
  {
    label: "Gaspillage de denrées comestibles",
    key: "unservedEdibleMass",
  },
  {
    label: "Gaspillage de denrées non comestibles",
    key: "unservedInedibleMass",
  },
  {
    heading: "Reste assiette",
  },
  {
    label: "Gaspillage total",
    key: "leftoversTotalMass",
  },
  {
    label: "Gaspillage de denrées comestibles",
    key: "leftoversEdibleMass",
  },
  {
    label: "Gaspillage de denrées non comestibles",
    key: "leftoversInedibleMass",
  },
]
</script>

<template>
  <div>
    <div v-for="field in detailedFields" :key="field.key" :class="field.tooltip ? 'calculated-field' : 'detail'">
      <p v-if="field.tooltip" class="fr-grid-row fr-grid-row--middle">
        {{ field.label }}
        <DsfrTooltip v-if="field.tooltip" :content="field.tooltip" />
      </p>
      <p v-else-if="field.label" class="fr-mb-1w">{{ field.label }}</p>
      <h4 v-else-if="field.heading" class="fr-h6 fr-mt-6w">{{ field.heading }}</h4>
      <p v-if="field.key">
        <b>
          {{ formatNumber(props.measurement[field.key]) }}
          {{ field.unit || "kg" }}
        </b>
      </p>
    </div>
  </div>
</template>

<style scoped>
div.detail {
  color: var(--text-mention-grey);
}
div.calculated-field {
  color: var(--text-default-info);
}
</style>
