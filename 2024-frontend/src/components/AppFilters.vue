<script setup>
import { ref } from "vue"
import { getYearsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Display */
const props = defineProps(["filters"])
const displayYearFilter = ref(props.filters.includes("year"))

/* Otions */
const yearsOptions = displayYearFilter.value ? ref(getYearsOptions()) : ref()

/* Models */
const yearModel = ref("")
</script>

<template>
  <ul class="ma-cantine--unstyled-list">
    <li v-if="displayYearFilter">
      <AppDropdown label="Années">
        <DsfrRadioButtonSet :modelValue="yearModel" :options="yearsOptions" small />
      </AppDropdown>
    </li>
  </ul>
</template>
