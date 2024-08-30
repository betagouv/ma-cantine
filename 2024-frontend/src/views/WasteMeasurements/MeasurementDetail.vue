<script setup>
import { formatNoValue } from "@/utils"

const props = defineProps(["measurement"])

const detailedFields = [
  {
    key: "totalMass",
    label: "Masse totale de gaspillage relevée sur la période de mesure",
  },
  // TODO: calculated value - from backend?
  // {
  //   label: "Période de mesure de mon gaspillage alimentaire",
  //   unit: "jours",
  // },
  {
    label: "Nombre de couverts sur la période",
    unit: "couverts",
    key: "mealCount",
  },
  // TODO: calculated value with tooltip - from backend?
  // {
  //   label: "Masse totale de gaspillage sur l'année",
  //   unit: "kg",
  // },
  {
    heading: "Mesure du gaspillage au niveau des excédents de préparation",
  },
  {
    label: "Masse de gaspillage d'excédents de préparation",
    key: "preparationTotalMass",
  },
  {
    label: "Masse de gaspillage de denrées comestibles parmi les excédents de préparation",
    key: "preparationEdibleMass",
  },
  {
    label: "Masse de gaspillage de denrées non comestibles parmi les excédents de préparation",
    key: "preparationInedibleMass",
  },
  {
    heading: "Mesure du gaspillage au niveau des denrées présentées aux convives mais non servies",
  },
  {
    label: "Masse de gaspillage de denrées présentées aux convives mais non servies",
    key: "unservedTotalMass",
  },
  {
    label: "Masse de gaspillage de denrées comestibles parmi les denrées présentées aux convives mais non servies",
    key: "unservedEdibleMass",
  },
  {
    label: "Masse de gaspillage de denrées non comestibles parmi les denrées présentées aux convives mais non servies",
    key: "unservedInedibleMass",
  },
  {
    heading: "Mesure du gaspillage au niveau du reste assiette",
  },
  {
    label: "Masse de gaspillage pour le reste assiette",
    key: "leftoversTotalMass",
  },
  {
    label: "Masse de gaspillage de denrées comestibles parmi le reste assiette",
    key: "leftoversEdibleMass",
  },
  {
    label: "Masse de gaspillage de denrées non comestibles parmi le reste assiette",
    key: "leftoversInedibleMass",
  },
]
</script>

<template>
  <div>
    <div v-for="field in detailedFields" :key="field.key" class="detail">
      <p v-if="field.label" class="fr-mb-1w">{{ field.label }}</p>
      <h4 v-else-if="field.heading" class="fr-h6">{{ field.heading }}</h4>
      <p v-if="field.key">
        <b>
          {{ formatNoValue(props.measurement[field.key]) }}
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
</style>
