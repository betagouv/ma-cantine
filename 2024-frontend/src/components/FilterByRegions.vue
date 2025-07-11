<script setup>
import { ref, computed } from "vue"
import { getRegionsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const regionsSelected = ref([])

/* Get regions */
const regions = ref(getRegionsOptions())

/* Search */
const search = ref("")
const options = computed(() => {
  if (regions.value.length === 0) return []
  if (search.value === "") return regions.value
  const searchedRegions = regions.value.filter((region) => {
    const name = region.label.toLowerCase()
    const stringSearched = search.value.toLowerCase()
    return name.indexOf(stringSearched) >= 0
  })
  return searchedRegions
})
</script>

<template>
  <AppDropdown label="Régions">
    <DsfrSearchBar
      :modelValue="search"
      placeholder="Rechercher une région"
      @update:modelValue="($event) => (search = $event)"
    />
    <DsfrCheckboxSet :modelValue="regionsSelected" :options="options" small />
  </AppDropdown>
</template>
