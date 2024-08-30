<script setup>
import { computed, onMounted, ref } from "vue"
// import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"

const props = defineProps(["canteenUrlComponent"])
const canteenId = computed(() => props.canteenUrlComponent.split("--")[0])
// TODO: populate canteen title from id via fetching canteen (should be in initial data summaries)

const newMeasurementRoute = {
  name: "DiagnosticTunnel",
  params: { canteenUrlComponent: props.canteenUrlComponent, year: 2024, measureId: "gaspillage-alimentaire" },
}

const measurementTunnel = computed(() => ({
  name: "DiagnosticTunnel",
  params: {
    canteenUrlComponent: props.canteenUrlComponent,
    year: 2024,
    measureId: "gaspillage-alimentaire",
    id: measurement.value.id,
  },
}))

const measurements = ref([])
const chosenMeasurementIdx = ref(0)
const measurement = computed(() => measurements.value.length && measurements.value[chosenMeasurementIdx.value])
const measurementChoices = computed(() => {
  return measurements.value.map((m, idx) => {
    return {
      // TODO: improve date formatting
      text: `${m.periodStartDate} - ${m.periodEndDate}`,
      value: idx,
    }
  })
})

const wastePerMeal = computed(() => {
  const m = measurement.value
  if (m && m.totalMass && m.mealCount) return (m.totalMass / m.mealCount) * 1000 // convert kg to g
  return undefined
})
const measurementPercentageValues = computed(() => {
  const m = measurement.value
  if (m && m.totalMass) {
    return {
      preparation: ((m.preparationTotalMass || 0) / m.totalMass) * 100,
      unserved: ((m.unservedTotalMass || 0) / m.totalMass) * 100,
      leftovers: ((m.leftoversTotalMass || 0) / m.totalMass) * 100,
      // TODO: other ?
    }
  }
  return undefined
})

const detailsExpandedId = ref("")
const detailedFields = [
  {
    key: "periodStartDate",
    label: "Date du pesage",
  },
  {
    key: "totalMass",
    label: "Total",
  },
]

onMounted(() => {
  fetch(`/api/v1/canteens/${canteenId.value}/wasteMeasurements`)
    .then((response) => response.json())
    .then((response) => {
      measurements.value = response
    })
})
</script>

<template>
  <div>
    <!-- TODO: fix circular import of breadcrumbs nav for hot reloading -->
    <!-- <BreadcrumbsNav :links="[{ title: 'Mon tableau de bord', to: { name: 'ManagementPage' } }]" /> -->
    <h1>Gaspillage alimentaire</h1>
    <p>
      Cantine : {{ canteenId }}
      <router-link :to="{ name: 'ManagementPage' }" class="fr-btn fr-btn--tertiary fr-btn--sm">
        Changer d'établissement
      </router-link>
    </p>
    <h2>Mon gaspillage mesuré</h2>
    <div v-if="measurements.length">
      <div v-if="measurement" class="fr-grid-row">
        <div class="fr-col-6">
          <!-- redudent to include "et par convive?" -->
          <!-- TODO: styling -->
          <p v-if="wastePerMeal">{{ wastePerMeal }} g par repas et par convive</p>
          <div class="fr-col-12 fr-col-sm-8 fr-mb-2w">
            <DsfrSelect v-model="chosenMeasurementIdx" label="Date du pesage" :options="measurementChoices" />
          </div>
          <router-link :to="newMeasurementRoute" class="fr-btn fr-btn--secondary">
            Saisir un nouveau pesage
          </router-link>
        </div>
        <div class="fr-col-6 fr-col-center">
          <div v-if="measurement.isSortedBySource">
            <!-- TODO: make graph -->
            <h3>Origine du gaspillage</h3>
            <ul v-if="measurementPercentageValues">
              <li>Excédents de préparation : {{ measurementPercentageValues.preparation }} %</li>
              <li>Denrées présentées mais non servies : {{ measurementPercentageValues.unserved }} %</li>
              <li>Reste-assiette : {{ measurementPercentageValues.leftovers }} %</li>
            </ul>
          </div>
          <div v-else>
            <DsfrAlert>
              Triez votre gaspillage alimentaire par source pour mieux comprendre comment agir.
            </DsfrAlert>
          </div>
        </div>
      </div>
      <DsfrAccordion
        id="waste-measurement-detail"
        title="Données détaillées"
        :expanded-id="detailsExpandedId"
        @expand="detailsExpandedId = $event"
        class="fr-my-4w"
      >
        <!-- TODO: complete info and styling -->
        <div class="fr-grid-row">
          <div class="fr-col-12 fr-col-sm-8">
            <div v-for="field in detailedFields" :key="field.key">
              <p>{{ field.label }}</p>
              <p>{{ measurement[field.key] }}</p>
            </div>
          </div>
          <!-- TODO: align to right -->
          <div class="fr-col-12 fr-col-sm-4">
            <router-link class="fr-btn fr-btn--tertiary" :to="measurementTunnel">Modifier les données</router-link>
          </div>
        </div>
      </DsfrAccordion>
    </div>
    <div v-else>
      <p>
        Votre établissement est soumis à l'obligation de faire une analyse des causes du gaspillage alimentaire, et de
        mettre en place une démarche de lutte contre le gaspillage alimentaire.
      </p>
      <DsfrBadge label="Pas encore des données" type="none" />
      <!-- TODO: styling -->
      <p>- g par repas et par convive</p>
      <router-link :to="newMeasurementRoute" class="fr-btn">
        Saisir un pesage
      </router-link>
    </div>
    <!-- TODO: show first few actions ? -->
    <h2 class="fr-mt-4w">Agir contre le gaspillage alimentaire</h2>
    <router-link
      :to="{ name: 'WasteActionsHome' }"
      :class="{ 'fr-btn': true, 'fr-btn--secondary': !measurements.length }"
    >
      Actions
    </router-link>
  </div>
</template>
