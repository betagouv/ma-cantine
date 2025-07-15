<script setup>
import { ref, computed } from "vue"
import { getDepartmentsOptionsFromSearch } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const departementsSelected = ref([])

/* Get departments */
const departments = ref(getDepartmentsOptionsFromSearch())

/* Search */
const search = ref("")
const options = computed(() => {
  if (departments.value.length === 0) return []
  return getDepartmentsOptionsFromSearch(search.value)
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
