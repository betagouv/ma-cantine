<script setup>
import { ref, computed } from "vue"
import { getPATOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Model */
const PATSelected = ref([])

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
    <DsfrCheckboxSet :modelValue="PATSelected" :options="options" small />
  </AppDropdown>
</template>
