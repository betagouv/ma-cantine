<script setup>
import { computed, ref } from "vue"
import { formatNumber, getSum } from "@/utils"

const props = defineProps(["measurement"])

const measurementSumValues = computed(() => {
  const m = props.measurement
  const hasAtLeastOneEdibleMass = m.preparationEdibleMass || m.unservedEdibleMass || m.leftoversEdibleMass
  if (hasAtLeastOneEdibleMass) {
    return {
      edible: getSum([m.preparationEdibleMass, m.unservedEdibleMass, m.leftoversEdibleMass]),
      inedible: getSum([m.preparationInedibleMass, m.unservedInedibleMass, m.leftoversInedibleMass]),
    }
  }
  return undefined
})

const measurementGraphValues = computed(() => {
  return {
    y: JSON.stringify([measurementSumValues.value.edible, measurementSumValues.value.inedible]),
    x: JSON.stringify(["Comestible", "Non-comestible"]),
  }
})

const displayOption = ref("chart")
</script>

<template>
  <div v-if="measurementSumValues">
    <div class="fr-grid-row">
      <div class="fr-col-md-7 fr-mb-2w">
        <h3 class="fr-h6 fr-my-0">Part de comestible</h3>
      </div>
      <div class="fr-col fr-mb-2w">
        <div class="fr-grid-row">
          <DsfrSegmentedSet
            name="Part de comestible"
            label="Choix d'affichage"
            :options="[
              {
                label: 'Charte',
                value: 'chart',
              },
              {
                label: 'Texte',
                value: 'text',
              },
            ]"
            v-model="displayOption"
            small
          />
        </div>
      </div>
    </div>
    <div v-if="displayOption === 'chart'" class="fr-py-2w fr-pr-8w">
      <pie-chart
        :name="measurementGraphValues.x"
        :x="measurementGraphValues.x"
        :y="measurementGraphValues.y"
        color='["green-bourgeon", "orange-terre-battue"]'
      ></pie-chart>
    </div>
    <div v-else-if="displayOption === 'text'">
      <ul>
        <li>Comestible : {{ formatNumber(measurementSumValues.edible) }} kg</li>
        <li>Non-comestible : {{ formatNumber(measurementSumValues.inedible) }} kg</li>
      </ul>
    </div>
  </div>
  <DsfrAlert v-else>
    Completez l'évaluation pour visualiser la part de comestible de votre gaspillage.
  </DsfrAlert>
</template>
