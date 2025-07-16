<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getYearsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const options = ref(getYearsOptions())
const storeFilters = useStoreFilters()
const yearSelected = computed(() => storeFilters.get("year"))
</script>

<template>
  <AppDropdown label="Années">
    <DsfrRadioButtonSet
      :modelValue="yearSelected"
      @update:modelValue="storeFilters.add('year', $event)"
      :options="options"
      small
    />
  </AppDropdown>
</template>
