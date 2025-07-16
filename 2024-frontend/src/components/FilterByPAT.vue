<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getPATOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const storeFilters = useStoreFilters()
const PATSelected = computed(() => storeFilters.params.pats)

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getPATOptionsFromSearch(search.value)
})
</script>
<template>
  <AppDropdown label="PAT">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un PAT" />
    <DsfrCheckboxSet
      :modelValue="PATSelected"
      @update:modelValue="storeFilters.add('pats', value)"
      :options="options"
      small
    />
  </AppDropdown>
</template>
