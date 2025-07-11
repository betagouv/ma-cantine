<script setup>
import { ref, computed } from "vue"
import { getPATOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Model */
const selectedPAT = ref([])

/* Search */
const search = ref("")
const options = computed(() => {
  if (search.value.length === 0) return []
  return getPATOptionsFromSearch(search.value)
})
</script>
<template>
  <AppDropdown label="PAT">
    <DsfrSearchBar
      :modelValue="search"
      placeholder="Rechercher un PAT"
      @update:modelValue="($event) => (search = $event)"
    />
    <DsfrCheckboxSet :modelValue="selectedPAT" :options="options" small />
  </AppDropdown>
</template>
