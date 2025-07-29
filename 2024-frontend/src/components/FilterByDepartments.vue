<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getDepartmentsOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const departments = ref(getDepartmentsOptionsFromSearch())
const storeFilters = useStoreFilters()
const departmentsSelected = computed(() => storeFilters.getParam("departments"))

/* Search */
const search = ref("")
const options = computed(() => {
  if (departments.value.length === 0) return []
  return getDepartmentsOptionsFromSearch(search.value)
})
</script>

<template>
  <FilterByBase label="Départements">
    <DsfrSearchBar v-model="search" placeholder="Rechercher un département" />
    <DsfrCheckboxSet
      :modelValue="departmentsSelected"
      @update:modelValue="storeFilters.set('departments', $event)"
      :options="options"
      small
    />
  </FilterByBase>
</template>
