<script setup>
import { ref, computed } from "vue"
import { getSectorsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const sectorsSelected = ref([])

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
  <AppDropdown label="Secteurs">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un secteur" />
    <DsfrCheckboxSet :modelValue="sectorsSelected" :options="options" small />
  </AppDropdown>
</template>
