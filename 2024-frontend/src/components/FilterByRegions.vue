<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getRegionsOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Get regions */
const regions = ref(getRegionsOptionsFromSearch())

/* Search */
const search = ref("")
const options = computed(() => {
  if (regions.value.length === 0) return []
  return getRegionsOptionsFromSearch(search.value)
})

/* Selected regions */
const storeFilters = useStoreFilters()
const regionsSelected = computed(() => storeFilters.params.regions)
const updateFilter = (value) => {
  storeFilters.add("regions", value)
}
</script>

<template>
  <AppDropdown label="Régions">
    <DsfrSearchBar v-model="search" placeholder="Rechercher une région" />
    <DsfrCheckboxSet :modelValue="regionsSelected" @update:modelValue="updateFilter" :options="options" small />
  </AppDropdown>
</template>
