<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getEPCIOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const EPCIsSelected = computed(() => storeFilters.getParam("epcis"))

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getEPCIOptionsFromSearch(search.value)
})
</script>
<template>
  <FilterByBase label="EPCI">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un EPCI" />
    <DsfrCheckboxSet
      :modelValue="EPCIsSelected"
      @update:modelValue="storeFilters.set('epcis', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
