<script setup>
import { ref, computed } from "vue"
import { getCitiesOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Model */
const citiesSelected = ref([])

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getCitiesOptionsFromSearch(search.value)
})
</script>
<template>
  <AppDropdown label="Communes">
    <DsfrSearchBar v-model="search" placeholder="Rechercher une commune" />
    <DsfrCheckboxSet :modelValue="citiesSelected" :options="options" small />
  </AppDropdown>
</template>
