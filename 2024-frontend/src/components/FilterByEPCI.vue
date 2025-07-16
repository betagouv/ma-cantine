<script setup>
import { ref, computed } from "vue"
import { getEPCIOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Model */
const EPCISelected = ref([])

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getEPCIOptionsFromSearch(search.value)
})
</script>
<template>
  <AppDropdown label="EPCI">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un EPCI" />
    <DsfrCheckboxSet :modelValue="EPCISelected" :options="options" small />
  </AppDropdown>
</template>
