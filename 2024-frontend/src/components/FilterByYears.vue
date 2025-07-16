<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getYearsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const storeFilters = useStoreFilters()
const yearSelected = computed(() => storeFilters.params.year)
const options = ref(getYearsOptions())
const updateFilter = (value) => {
  storeFilters.add("year", value)
}
</script>

<template>
  <AppDropdown label="Années">
    <DsfrRadioButtonSet :modelValue="yearSelected" @update:modelValue="updateFilter" :options="options" small />
  </AppDropdown>
</template>
