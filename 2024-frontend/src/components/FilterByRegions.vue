<script setup>
import { ref, computed } from "vue"
import { getRegionsOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const regionsSelected = ref([])

/* Get regions */
const regions = ref(getRegionsOptionsFromSearch())

/* Search */
const search = ref("")
const options = computed(() => {
  if (regions.value.length === 0) return []
  return getRegionsOptionsFromSearch(search.value)
})
</script>

<template>
  <AppDropdown label="Régions">
    <DsfrSearchBar v-model="search" placeholder="Rechercher une région" />
    <DsfrCheckboxSet :modelValue="regionsSelected" :options="options" small />
  </AppDropdown>
</template>
