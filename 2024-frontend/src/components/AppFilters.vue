<script setup>
import { ref, computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { getYearsOptions, getCharacteristicsOptions, getSectorsOptions } from "@/services/filters"
import openDataService from "@/services/openData"
import AppDropdown from "@/components/AppDropdown.vue"

/* Display */
const props = defineProps(["filters"])
const displayYearFilter = ref(props.filters.includes("years"))
const displayCharacteristicsFilter = ref(props.filters.includes("characteristics"))
const displaySectorsFilter = ref(props.filters.includes("sectors"))
const displayCitiesFilter = ref(props.filters.includes("cities"))

/* Models */
const yearModel = ref("")
const economicModel = ref([])
const managementType = ref([])
const productionType = ref([])
const sectors = ref([])
const searchSectors = ref("")
const searchCities = ref("")

/* Otions */
const yearsOptions = ref(getYearsOptions())
const characteristicsOptions = ref(getCharacteristicsOptions())
const allSectorsOptions = ref([])
getSectorsOptions().then((response) => {
  allSectorsOptions.value = response
})

/* Search sectors */
const sectorsOptions = computed(() => {
  if (allSectorsOptions.value.length === 0) return []
  if (searchSectors.value === "") return allSectorsOptions.value
  const searchedSectors = allSectorsOptions.value.filter((sector) => {
    const sectorLabel = sector.label.toLowerCase()
    const stringSearched = searchSectors.value.toLowerCase()
    return sectorLabel.indexOf(stringSearched) >= 0
  })
  return searchedSectors
})

/* Cities */
const citiesOptions = computedAsync(async () => {
  const response = await openDataService.findCitiesWithNameAutocompletion(searchCities.value)
  const citiesCheckboxes = response.map((city) => {
    return {
      label: `${city.nom} (${city.codeDepartement})`,
      value: city.code,
      id: city.code,
    }
  })
  return citiesCheckboxes
})
</script>

<template>
  <div class="app-filters">
    <p class="app-filters__title fr-mb-0">Filtrer par :</p>
    <ul class="ma-cantine--unstyled-list fr-grid-row">
      <li class="fr-mr-1w">
        <AppDropdown label="Régions"></AppDropdown>
      </li>
      <li class="fr-mr-1w">
        <AppDropdown label="Départements"></AppDropdown>
      </li>
      <li class="fr-mr-1w">
        <AppDropdown label="EPCI"></AppDropdown>
      </li>
      <li class="fr-mr-1w">
        <AppDropdown label="PAT"></AppDropdown>
      </li>
      <li v-if="displayCitiesFilter" class="fr-mr-1w">
        <AppDropdown label="Communes">
          <DsfrSearchBar
            :modelValue="searchCities"
            placeholder="Rechercher une commune"
            @update:modelValue="($event) => (searchCities = $event)"
          />
          <DsfrCheckboxSet :modelValue="sectors" :options="citiesOptions" small />
        </AppDropdown>
      </li>
      <li class="fr-hidden fr-unhidden-md fr-col-12"></li>
      <li v-if="displaySectorsFilter" class="fr-mr-1w">
        <AppDropdown label="Secteurs">
          <DsfrSearchBar
            :modelValue="searchSectors"
            placeholder="Rechercher un secteur"
            @update:modelValue="($event) => (searchSectors = $event)"
          />
          <DsfrCheckboxSet :modelValue="sectors" :options="sectorsOptions" small />
        </AppDropdown>
      </li>
      <li v-if="displayCharacteristicsFilter" class="fr-mr-1w">
        <AppDropdown label="Caractéristiques">
          <DsfrCheckboxSet
            legend="Types d’établissement :"
            :modelValue="economicModel"
            :options="characteristicsOptions.economicModel"
            small
            inline
          />
          <DsfrCheckboxSet
            legend="Modes de gestion :"
            :modelValue="managementType"
            :options="characteristicsOptions.managementType"
            small
            inline
          />
          <DsfrCheckboxSet
            legend="Modes de production :"
            :modelValue="productionType"
            :options="characteristicsOptions.productionType"
            small
            inline
          />
        </AppDropdown>
      </li>
      <li v-if="displayYearFilter" class="fr-mr-1w">
        <AppDropdown label="Années" class="size-small">
          <DsfrRadioButtonSet :modelValue="yearModel" :options="yearsOptions" small />
        </AppDropdown>
      </li>
    </ul>
  </div>
</template>

<style lang="scss">
.app-filters {
  display: flex;
  justify-content: flex-start;
  align-items: baseline;
  flex-direction: column;
  gap: 1rem;

  @media (min-width: 768px) {
    flex-direction: row;
  }

  &__title {
    flex-shrink: 0;
  }
}
</style>
