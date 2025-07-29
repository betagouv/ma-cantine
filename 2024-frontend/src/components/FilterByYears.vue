<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getYearsOptions } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const options = ref(getYearsOptions())
const storeFilters = useStoreFilters()
const yearSelected = computed(() => storeFilters.get("year")[0].value)
</script>

<template>
  <FilterByBase label="Années">
    <DsfrRadioButtonSet
      :modelValue="yearSelected"
      @update:modelValue="storeFilters.set('year', [{ value: $event, label: $event }])"
      :options="options"
      small
    />
  </FilterByBase>
</template>
