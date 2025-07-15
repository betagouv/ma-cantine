<script setup>
import { ref, computed } from "vue"
import { useFiltersStore } from "@/stores/filters"
import { getYearsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const filterStore = useFiltersStore()
const yearSelected = computed(() => filterStore.year)
const options = ref(getYearsOptions())
const updateFilter = (value) => {
  filterStore.update("year", value)
}
</script>

<template>
  <AppDropdown label="Années">
    <DsfrRadioButtonSet :modelValue="yearSelected" @update:modelValue="updateFilter" :options="options" small />
  </AppDropdown>
</template>
