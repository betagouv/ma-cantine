<script setup>
import { ref } from "vue"
import AppDropdown from "@/components/AppDropdown.vue"

/* Model */
const selectedCities = ref("")

/* Search */
const search = ref("")
</script>
<template>
  <AppDropdown label="Communes">
    <DsfrSearchBar
      :modelValue="search"
      placeholder="Rechercher une commune"
      @update:modelValue="($event) => (search = $event)"
    />
    <DsfrCheckboxSet :modelValue="selectedCities" :options="[]" small />
  </AppDropdown>
</template>
