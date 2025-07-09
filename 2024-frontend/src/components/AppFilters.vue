<script setup>
import { ref, computed } from "vue"
import { getYearsOptions, getCharacteristicsOptions, getSectorsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Display */
const props = defineProps(["filters"])
const displayYearFilter = ref(props.filters.includes("years"))
const displayCharacteristicsFilter = ref(props.filters.includes("characteristics"))
const displaySectorsFilter = ref(props.filters.includes("sectors"))

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
  if (searchSectorsString.value === "") return allSectorsOptions.value
  const searchedSectors = allSectorsOptions.value.filter((sector) => {
    const sectorLabel = sector.label.toLowerCase()
    const stringSearched = searchSectorsString.value.toLowerCase()
    return sectorLabel.indexOf(stringSearched) >= 0
  })
  return searchedSectors
})
const updateSearch = (string) => {
  searchSectorsString.value = string
}

/* Models */
const yearModel = ref("")
const economicModel = ref([])
const managementType = ref([])
const productionType = ref([])
const sectors = ref([])
const searchSectorsString = ref("")
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
      <li class="fr-mr-1w">
        <AppDropdown label="Communes"></AppDropdown>
      </li>
      <li class="fr-hidden fr-unhidden-md fr-col-12"></li>
      <li v-if="displaySectorsFilter" class="fr-mr-1w">
        <AppDropdown label="Secteurs">
          <DsfrSearchBar
            :modelValue="searchSectorsString"
            placeholder="Rechercher un secteur"
            @update:modelValue="updateSearch"
          />
          <DsfrCheckboxSet :modelValue="sectors" :options="sectorsOptions" small />
        </AppDropdown>
      </li>
      <li v-if="displayCharacteristicsFilter" class="fr-mr-1w">
        <AppDropdown label="Caractéristiques des cantines">
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
