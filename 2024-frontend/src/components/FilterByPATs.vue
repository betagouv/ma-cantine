<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getPATOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const storeFilters = useStoreFilters()
const PATsSelected = computed(() => storeFilters.getParam("pats"))
const route = useRoute()

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
    <DsfrSearchBar v-model="search" placeholder="Rechercher un PAT" />
    <DsfrCheckboxSet
      :modelValue="PATsSelected"
      @update:modelValue="storeFilters.set('pats', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
