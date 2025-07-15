<script setup>
import { ref } from "vue"
import { getYearsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const selectedYear = ref("")
const options = ref(getYearsOptions())
</script>

<template>
  <AppDropdown label="Années">
    <DsfrRadioButtonSet :modelValue="selectedYear" :options="options" small />
  </AppDropdown>
</template>
