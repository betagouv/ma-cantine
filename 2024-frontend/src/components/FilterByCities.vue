<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getCitiesOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const citiesSelected = computed(() => storeFilters.getParam("cities"))

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getCitiesOptionsFromSearch(search.value)
})
</script>
<template>
  <FilterByBase label="Communes">
    <DsfrSearchBar v-model="search" placeholder="Rechercher une commune" />
    <DsfrCheckboxSet
      :modelValue="citiesSelected"
      @update:modelValue="storeFilters.set('cities', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
