<script setup>
import { ref, computed } from "vue"
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

/* Prefill filters from query */
const query = route.query
const allRegions = getRegionsOptionsFromSearch()
if (query.regions) storeFilters.setFromQuery("regions", query.regions, allRegions)
if (query.region) storeFilters.setFromQuery("regions", query.region, allRegions) // Redirect from vue2
</script>

<template>
  <FilterByBase label="Régions">
    <DsfrSearchBar v-model="search" placeholder="Rechercher une région" />
    <p v-if="search.length > 0 && options.length === 0" class="fr-error-text fr-mb-0">Aucune région trouvée pour la recherche « {{ search }} »</p>
    <DsfrCheckboxSet
      v-if="options.length > 0"
      :modelValue="regionsSelected"
      @update:modelValue="storeFilters.set('regions', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
