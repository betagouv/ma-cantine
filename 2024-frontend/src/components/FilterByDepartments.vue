<script setup>
import { ref, computed } from "vue"
import { getDepartmentsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const departementsSelected = ref([])

/* Get departments */
const departments = ref(getDepartmentsOptions())

/* Search */
const search = ref("")
const options = computed(() => {
  if (departments.value.length === 0) return []
  if (search.value === "") return departments.value
  const searchedDepartments = departments.value.filter((department) => {
    const departmentName = department.label.toLowerCase()
    const stringSearched = search.value.toLowerCase()
    return departmentName.indexOf(stringSearched) >= 0
  })
  return searchedDepartments
})
</script>

<template>
  <AppDropdown label="Département">
    <DsfrSearchBar
      :modelValue="search"
      placeholder="Rechercher un département"
      @update:modelValue="($event) => (search = $event)"
    />
    <DsfrCheckboxSet :modelValue="departementsSelected" :options="options" small />
  </AppDropdown>
</template>
