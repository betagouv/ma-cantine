<script setup>
import { formatNumber } from "@/utils"
import Constants from "@/constants.js"

const props = defineProps(["measurement"])

const detailedFields = [
  {
    key: "totalMass",
    label: Constants.WasteMeasurement.totalMass.title,
  },
  {
    key: "daysInPeriod",
    label: Constants.WasteMeasurement.daysInPeriod.title,
    unit: "jours",
  },
  {
    key: "mealCount",
    label: Constants.WasteMeasurement.mealCount.title,
    unit: "couverts",
  },
  {
    key: "totalYearlyWasteEstimation",
    label: "Masse totale de déchets alimentaires sur l'année",
    unit: "kg",
    tooltip:
      "Calculé en prenant les déchets alimentaires par repas pour la période, multiplié par le nombre de couverts par année pour l'établissement",
  },
  {
    heading: Constants.WasteMeasurement.preparation.title,
  },
  {
    label: "Total",
    key: "preparationTotalMass",
  },
  {
    label: "Denrées comestibles",
    key: "preparationEdibleMass",
  },
  {
    label: "Denrées non comestibles",
    key: "preparationInedibleMass",
  },
  {
    heading: Constants.WasteMeasurement.unserved.title,
  },
  {
    label: "Total",
    key: "unservedTotalMass",
  },
  {
    label: "Denrées comestibles",
    key: "unservedEdibleMass",
  },
  {
    label: "Denrées non comestibles",
    key: "unservedInedibleMass",
  },
  {
    heading: Constants.WasteMeasurement.leftovers.title,
  },
  {
    label: "Total",
    key: "leftoversTotalMass",
  },
  {
    label: "Denrées comestibles",
    key: "leftoversEdibleMass",
  },
  {
    label: "Denrées non comestibles",
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
