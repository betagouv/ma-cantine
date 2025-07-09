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
const economicModel = ref("")
const managementType = ref("")
const productionType = ref([])
const sectors = ref([])
const searchSectorsString = ref("")
</script>

<template>
  <div class="fr-grid-row fr-grid-row--left fr-grid-row--middle">
    <p class="fr-mb-0 fr-mr-2w">Filtrer par :</p>
    <ul class="ma-cantine--unstyled-list fr-grid-row">
      <li v-if="displaySectorsFilter" class="fr-mr-1v">
        <AppDropdown label="Secteurs">
          <DsfrSearchBar
            :modelValue="searchSectorsString"
            placeholder="Rechercher un secteur"
            @update:modelValue="updateSearch"
          />
          <DsfrCheckboxSet :modelValue="sectors" :options="sectorsOptions" small />
        </AppDropdown>
      </li>
      <li v-if="displayCharacteristicsFilter" class="fr-mr-1v">
        <AppDropdown label="Caractéristiques">
          <DsfrRadioButtonSet
            legend="Type d’établissement"
            :modelValue="economicModel"
            :options="characteristicsOptions.economicModel"
            small
            inline
          />
          <DsfrRadioButtonSet
            legend="Mode de gestion"
            :modelValue="managementType"
            :options="characteristicsOptions.managementType"
            small
            inline
          />
          <DsfrCheckboxSet
            legend="Modes de production"
            :modelValue="productionType"
            :options="characteristicsOptions.productionType"
            small
          />
        </AppDropdown>
      </li>
      <li v-if="displayYearFilter" class="fr-mr-1v">
        <AppDropdown label="Années" class="size-small">
          <DsfrRadioButtonSet :modelValue="yearModel" :options="yearsOptions" small />
        </AppDropdown>
      </li>
    </ul>
  </div>
</template>
