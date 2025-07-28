<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getSectorsOptions } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const sectorsSelected = computed(() => storeFilters.get("sectors"))

/* Get sectors */
const sectors = ref([])
getSectorsOptions().then((response) => {
  sectors.value = response
})

/* Search */
const search = ref("")
const options = computed(() => {
  if (sectors.value.length === 0) return []
  if (search.value === "") return sectors.value
  const searchedSectors = sectors.value.filter((sector) => {
    const sectorLabel = sector.label.toLowerCase()
    const stringSearched = search.value.toLowerCase()
    return sectorLabel.indexOf(stringSearched) >= 0
  })
  return searchedSectors
})
</script>

<template>
  <FilterByBase label="Secteurs">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un secteur" />
    <DsfrCheckboxSet
      :modelValue="sectorsSelected"
      @update:modelValue="storeFilters.set('sectors', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
