<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getCharacteristicsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const economicModel = computed(() => storeFilters.params.economicModel)
const managementType = computed(() => storeFilters.params.managementType)
const productionType = computed(() => storeFilters.params.productionType)
const options = ref(getCharacteristicsOptions())

const storeFilters = useStoreFilters()
const updateFilter = (name, value) => {
  storeFilters.add(name, value)
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
