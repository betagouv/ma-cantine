<script setup>
import { ref } from "vue"
import { getYearsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const yearSelected = ref("")
const options = ref(getYearsOptions())
</script>

<template>
  <AppDropdown label="Années">
    <DsfrRadioButtonSet :modelValue="yearSelected" :options="options" small />
  </AppDropdown>
</template>
