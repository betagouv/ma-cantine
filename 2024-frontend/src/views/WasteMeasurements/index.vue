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

onMounted(() => {
  fetch(`/api/v1/canteens/${canteenId.value}/wasteMeasurements`)
    .then((response) => response.json())
    .then((response) => {
      measurements.value = response
    })
})

const formatNoValue = (value) => {
  if (value || value === 0) return value
  return "—"
}
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
          <p v-if="wastePerMeal" class="highlight brown">
            <span class="fr-h3">{{ wastePerMeal }} g</span>
            par repas et par convive
          </p>
          <router-link :to="newMeasurementRoute" class="fr-btn fr-btn--secondary">
            Saisir un nouveau pesage
          </router-link>
        </div>
        <div class="fr-col-6 fr-col-center">
          <div v-if="measurement.isSortedBySource">
            <!-- TODO: make graph -->
            <h3>Origine du gaspillage</h3>
            <ul v-if="measurementPercentageValues">
              <li>Excédents de préparation : {{ formatNoValue(measurementPercentageValues.preparation) }} %</li>
              <li>Denrées présentées mais non servies : {{ formatNoValue(measurementPercentageValues.unserved) }} %</li>
              <li>Reste-assiette : {{ formatNoValue(measurementPercentageValues.leftovers) }} %</li>
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
        <div class="fr-grid-row fr-grid-row--bottom fr-mb-4w">
          <div class="fr-col-12 fr-col-sm-6 fr-col-md-4 fr-pr-4w">
            <DsfrSelect v-model="chosenMeasurementIdx" label="Date du pesage" :options="measurementChoices" />
          </div>
          <div class="fr-col-12 fr-col-sm-4">
            <router-link class="fr-btn fr-btn--tertiary" :to="measurementTunnel">
              <span class="fr-icon-pencil-line fr-icon--sm fr-mr-1w"></span>
              Modifier les données
            </router-link>
          </div>
        </div>
        <div v-for="field in detailedFields" :key="field.key" class="detail">
          <p v-if="field.label" class="fr-mb-1w">{{ field.label }}</p>
          <h4 v-else-if="field.heading" class="fr-h6">{{ field.heading }}</h4>
          <p v-if="field.key">
            <b>
              {{ formatNoValue(measurement[field.key]) }}
              {{ field.unit || "kg" }}
            </b>
          </p>
        </div>
        <router-link class="fr-btn fr-btn--tertiary fr-btn--sm" :to="measurementTunnel">
          <span class="fr-icon-pencil-line fr-icon--sm fr-mr-1w"></span>
          Modifier les données
        </router-link>
      </DsfrAccordion>
    </div>
    <div v-else>
      <p>
        Votre établissement est soumis à l'obligation de faire une analyse des causes du gaspillage alimentaire, et de
        mettre en place une démarche de lutte contre le gaspillage alimentaire.
      </p>
      <DsfrBadge label="Pas encore des données" type="none" />
      <p class="fr-my-4w highlight">
        <span class="fr-h3">{{ formatNoValue() }} g</span>
        par repas et par convive
      </p>
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

<style scoped>
p.highlight {
  color: var(--text-mention-grey);
  display: flex;
  align-items: center;
}
p.highlight > span {
  border-radius: 18px;
  padding: 4px 16px;
  margin-right: 8px;
  margin-bottom: 0;

  background: var(--background-default-grey-hover);
  color: inherit;
}
p.highlight.brown {
  color: var(--text-action-high-orange-terre-battue);
}
p.highlight.brown > span {
  background: var(--orange-terre-battue-975-75);
}

div.detail {
  color: var(--text-mention-grey);
}
</style>
