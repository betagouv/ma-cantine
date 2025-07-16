<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getEPCIOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getEPCIOptionsFromSearch(search.value)
})

/* Selected EPCI */
const storeFilters = useStoreFilters()
const EPCISelected = computed(() => storeFilters.params.epcis)
const updateFilter = (value) => {
  storeFilters.add("epcis", value)
}
</script>
<template>
  <AppDropdown label="EPCI">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un EPCI" />
    <DsfrCheckboxSet :modelValue="EPCISelected" @update:modelValue="updateFilter" :options="options" small />
  </AppDropdown>
</template>
