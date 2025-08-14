<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getDepartmentsOptionsFromSearch } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const departments = ref(getDepartmentsOptionsFromSearch())
const storeFilters = useStoreFilters()
const departmentsSelected = computed(() => storeFilters.getParam("departments"))
const route = useRoute()

/* Search */
const search = ref("")
const options = computed(() => {
  if (departments.value.length === 0) return []
  return getDepartmentsOptionsFromSearch(search.value)
})

/* Prefill filters from query */
const query = route.query
const allDepartments = getDepartmentsOptionsFromSearch()
if (query.departments) storeFilters.setFromQuery("departments", query.departments, allDepartments)
if (query.department) storeFilters.setFromQuery("departments", query.department, allDepartments) // Redirect from vue2
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
