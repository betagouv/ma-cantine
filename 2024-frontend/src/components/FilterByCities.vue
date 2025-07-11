<script setup>
import { ref, computed } from "vue"
import { getCitiesOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Model */
const selectedCities = ref([])

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getCitiesOptionsFromSearch(search.value)
})
</script>
<template>
  <AppDropdown label="Communes">
    <DsfrSearchBar
      :modelValue="search"
      placeholder="Rechercher une commune"
      @update:modelValue="($event) => (search = $event)"
    />
    <DsfrCheckboxSet :modelValue="selectedCities" :options="options" small />
  </AppDropdown>
</template>
