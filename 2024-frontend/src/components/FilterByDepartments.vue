<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getDepartmentsOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Get departments */
const departments = ref(getDepartmentsOptionsFromSearch())

/* Search */
const search = ref("")
const options = computed(() => {
  if (departments.value.length === 0) return []
  return getDepartmentsOptionsFromSearch(search.value)
})

/* Selected departements */
const storeFilters = useStoreFilters()
const departementsSelected = computed(() => storeFilters.params.departements)
const updateFilter = (value) => {
  storeFilters.add("departements", value)
}
</script>

<template>
  <AppDropdown label="Département">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un département" />
    <DsfrCheckboxSet :modelValue="departementsSelected" @update:modelValue="updateFilter" :options="options" small />
  </AppDropdown>
</template>
