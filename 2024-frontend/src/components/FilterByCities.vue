<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getCitiesOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getCitiesOptionsFromSearch(search.value)
})

/* Select City */
const storeFilters = useStoreFilters()
const citiesSelected = computed(() => storeFilters.params.cities)
const updateFilter = (value) => {
  storeFilters.add("cities", value)
}
</script>
<template>
  <AppDropdown label="Communes">
    <DsfrSearchBar v-model="search" placeholder="Rechercher une commune" />
    <DsfrCheckboxSet :modelValue="citiesSelected" @update:modelValue="updateFilter" :options="options" small />
  </AppDropdown>
</template>
