<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getEPCIOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const storeFilters = useStoreFilters()
const EPCISelected = computed(() => storeFilters.get("epcis"))

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
    <DsfrCheckboxSet
      :modelValue="EPCISelected"
      @update:modelValue="storeFilters.add('epcis', $event)"
      :options="options"
      small
    />
  </AppDropdown>
</template>
