<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getPATOptionsFromSearch, getPATsCount } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const PATsSelected = computed(() => storeFilters.getParam("pats"))
const route = useRoute()

/* Count */
const count = computed(() => getPATsCount())

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getPATOptionsFromSearch(search.value)
})

/* Prefill filters from query */
const query = route.query
const allPATs = getPATOptionsFromSearch()
if (query.pats) storeFilters.setFromQuery("pats", query.pats, allPATs)
</script>
<template>
  <FilterByBase label="PAT">
    <p class="fr-mb-1w">
      {{ count }} PAT existants<br />
      <span class="fr-hint-text">Utilisez la barre de recherche pour sélectionner le ou les PAT souhaités.</span>
    </p>
    <DsfrSearchBar v-model="search" placeholder="Rechercher un PAT" />
    <p v-if="search.length > 0 && options.length === 0" class="fr-error-text fr-mb-0">Aucun PAT trouvé pour la recherche « {{ search }} »</p>
    <DsfrCheckboxSet
      v-if="options.length > 0"
      :modelValue="PATsSelected"
      @update:modelValue="storeFilters.set('pats', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
