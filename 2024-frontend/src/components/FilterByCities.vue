<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getCitiesOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const storeFilters = useStoreFilters()
const citiesSelected = computed(() => storeFilters.get("cities"))

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
    <DsfrCheckboxSet
      :modelValue="citiesSelected"
      @update:modelValue="storeFilters.set('cities', $event)"
      :options="options"
      small
    />
  </AppDropdown>
</template>
