<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getRegionsOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const regions = ref(getRegionsOptionsFromSearch())
const storeFilters = useStoreFilters()
const regionsSelected = computed(() => storeFilters.getParam("regions"))
const route = useRoute()

/* Search */
const search = ref("")
const options = computed(() => {
  if (regions.value.length === 0) return []
  return getRegionsOptionsFromSearch(search.value)
})

/* Select from url */
onMounted(() => {
  const query = route.query
  const allRegions = getRegionsOptionsFromSearch()
  if (query.regions) storeFilters.setFromQuery("regions", query.regions, allRegions)
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
