<script setup>
import { ref, computed } from "vue"
import { useFiltersStore } from "@/stores/filters"
import { getCharacteristicsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const economicModel = computed(() => filterStore.params.economicModel)
const managementType = computed(() => filterStore.params.managementType)
const productionType = computed(() => filterStore.params.productionType)
const options = ref(getCharacteristicsOptions())

const filterStore = useFiltersStore()
const updateFilter = (name, value) => {
  filterStore.add(name, value)
}
</script>

<template>
  <AppDropdown label="Caractéristiques">
    <DsfrCheckboxSet
      legend="Types d’établissement :"
      :modelValue="economicModel"
      @update:modelValue="updateFilter('economicModel', $event)"
      :options="options.economicModel"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Modes de gestion :"
      :modelValue="managementType"
      @update:modelValue="updateFilter('managementType', $event)"
      :options="options.managementType"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Modes de production :"
      :modelValue="productionType"
      @update:modelValue="updateFilter('productionType', $event)"
      :options="options.productionType"
      small
      inline
    />
  </AppDropdown>
</template>
