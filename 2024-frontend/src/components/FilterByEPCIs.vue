<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getEPCIOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const EPCIsSelected = computed(() => storeFilters.getParam("epcis"))
const route = useRoute()

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getEPCIOptionsFromSearch(search.value)
})

/* Select from url */
onMounted(() => {
  const query = route.query
  const allEPCIs = getEPCIOptionsFromSearch()
  if (query.epcis) storeFilters.setFromQuery("epcis", query.epcis, allEPCIs)
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
