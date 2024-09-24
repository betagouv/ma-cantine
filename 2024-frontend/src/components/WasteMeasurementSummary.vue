<script setup>
import { computed, ref } from "vue"
import SourceChart from "./SourceChart.vue"
import MeasurementDetail from "./MeasurementDetail.vue"
import EmphasiseText from "./EmphasiseText.vue"
import { formatNumber, formatDate } from "@/utils"

const props = defineProps(["measurement", "measurements", "editable", "canteenUrlComponent"])

const chosenMeasurementIdx = ref(0)
const displayMeasurement = computed(
  () => props.measurement || (props.measurements?.length && props.measurements[chosenMeasurementIdx.value])
)

const wastePerMeal = computed(() => {
  const m = displayMeasurement.value
  if (m && m.totalMass && m.mealCount) return (m.totalMass / m.mealCount) * 1000 // convert kg to g
  return undefined
})

const measurementChoices = computed(() => {
  return props.measurements.map((m, idx) => {
    return {
      text: `${formatDate(m.periodStartDate, {
        month: "short",
        day: "numeric",
      })} - ${formatDate(m.periodEndDate)}`,
      value: idx,
    }
  })
})

const newMeasurementRoute = {
  name: "WasteMeasurementTunnel",
  params: { canteenUrlComponent: props.canteenUrlComponent },
}

const measurementTunnel = computed(() => ({
  name: "WasteMeasurementTunnel",
  params: {
    canteenUrlComponent: props.canteenUrlComponent,
    id: displayMeasurement.value.id,
  },
}))

const activeAccordion = ref("")
</script>

<template>
  <div>
    <div v-if="displayMeasurement" class="fr-grid-row fr-grid-row--middle">
      <div class="fr-col fr-mb-4w">
        <EmphasiseText :emphasisText="`${formatNumber(wastePerMeal)} g`" contextText="par repas" class="brown" />
        <router-link v-if="editable" :to="newMeasurementRoute" class="fr-btn fr-btn--secondary fr-mt-sm-2w">
          Saisir une nouvelle évaluation
        </router-link>
      </div>
      <div class="fr-col-12 fr-col-sm-5 fr-mb-4w">
        <div v-if="displayMeasurement.isSortedBySource">
          <SourceChart :measurement="displayMeasurement" />
        </div>
        <div v-else>
          <DsfrAlert>
            Triez votre gaspillage alimentaire par source pour mieux comprendre comment agir.
          </DsfrAlert>
        </div>
      </div>
    </div>
    <DsfrAccordionsGroup v-model="activeAccordion">
      <DsfrAccordion id="waste-measurement-detail" title="Données détaillées" class="fr-my-2w">
        <div class="fr-grid-row fr-grid-row--bottom fr-mb-4w">
          <div class="fr-col-12 fr-col-sm-6 fr-col-md-4 fr-pr-4w">
            <DsfrSelect
              v-if="editable"
              v-model="chosenMeasurementIdx"
              label="Date de l'évaluation"
              :options="measurementChoices"
            />
          </div>
          <div v-if="editable" class="fr-col-12 fr-col-sm-4">
            <router-link class="fr-btn fr-btn--tertiary" :to="measurementTunnel">
              <span class="fr-icon-pencil-line fr-icon--sm fr-mr-1w"></span>
              Modifier les données
            </router-link>
          </div>
        </div>
        <MeasurementDetail :measurement="displayMeasurement" />
        <router-link v-if="editable" class="fr-btn fr-btn--tertiary fr-btn--sm" :to="measurementTunnel">
          <span class="fr-icon-pencil-line fr-icon--sm fr-mr-1w"></span>
          Modifier les données
        </router-link>
      </DsfrAccordion>
    </DsfrAccordionsGroup>
  </div>
</template>
