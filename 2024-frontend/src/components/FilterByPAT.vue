<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getPATOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getPATOptionsFromSearch(search.value)
})

/* Select PAT */
const storeFilters = useStoreFilters()
const PATSelected = computed(() => storeFilters.params.pats)
const updateFilter = (value) => {
  storeFilters.add("pats", value)
}
</script>
<template>
  <AppDropdown label="PAT">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un PAT" />
    <DsfrCheckboxSet :modelValue="PATSelected" @update:modelValue="updateFilter" :options="options" small />
  </AppDropdown>
</template>
