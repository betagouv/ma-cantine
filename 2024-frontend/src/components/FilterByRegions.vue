<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getRegionsOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const regions = ref(getRegionsOptionsFromSearch())
const storeFilters = useStoreFilters()
const regionsSelected = computed(() => storeFilters.getParam("regions"))

/* Search */
const search = ref("")
const options = computed(() => {
  if (regions.value.length === 0) return []
  return getRegionsOptionsFromSearch(search.value)
})
</script>

<template>
  <FilterByBase label="Régions">
    <DsfrSearchBar v-model="search" placeholder="Rechercher une région" />
    <DsfrCheckboxSet
      :modelValue="regionsSelected"
      @update:modelValue="storeFilters.set('regions', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
