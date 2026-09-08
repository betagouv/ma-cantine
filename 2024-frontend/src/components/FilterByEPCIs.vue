<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getEPCIOptionsFromSearch, getEPCIsCount } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const EPCIsSelected = computed(() => storeFilters.getParam("epcis"))
const route = useRoute()

/* Count */
const count = computed(() => getEPCIsCount())

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getEPCIOptionsFromSearch(search.value)
})

/* Prefill filters from query */
const query = route.query
const allEPCIs = getEPCIOptionsFromSearch()
if (query.epcis) storeFilters.setFromQuery("epcis", query.epcis, allEPCIs)
</script>
<template>
  <FilterByBase label="EPCI">
    <p class="fr-mb-1w">
      {{ count }} EPCI existants<br />
      <span class="fr-hint-text">Utilisez la barre de recherche pour sélectionner le ou les EPCI souhaités.</span>
    </p>
    <DsfrSearchBar v-model="search" placeholder="Rechercher un EPCI" />
    <p v-if="search.length > 0 && options.length === 0" class="fr-error-text fr-mb-0">Aucun EPCI trouvé pour la recherche « {{ search }} »</p>
    <DsfrCheckboxSet
      v-if="options.length > 0"
      :modelValue="EPCIsSelected"
      @update:modelValue="storeFilters.set('epcis', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
