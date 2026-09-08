<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getCitiesOptionsFromSearch, getCitiesCount } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const citiesSelected = computed(() => storeFilters.getParam("cities"))
const route = useRoute()

/* Count */
const count = computed(() => getCitiesCount())

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getCitiesOptionsFromSearch(search.value)
})

/* Prefill filters from query */
const query = route.query
const allCities = getCitiesOptionsFromSearch()
if (query.cities) storeFilters.setFromQuery("cities", query.cities, allCities)
</script>
<template>
  <FilterByBase label="Communes">
    <p class="fr-mb-1w">
      {{ count }} communes existantes<br />
      <span class="fr-hint-text">Utilisez la barre de recherche pour sélectionner la ou les communes souhaitées.</span>
    </p>
    <DsfrSearchBar v-model="search" placeholder="Rechercher une commune" />
    <p v-if="search.length > 0 && options.length === 0" class="fr-error-text fr-mb-0">Aucune commune trouvée pour la recherche « {{ search }} »</p>
    <DsfrCheckboxSet
      v-if="options.length > 0"
      :modelValue="citiesSelected"
      @update:modelValue="storeFilters.set('cities', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
