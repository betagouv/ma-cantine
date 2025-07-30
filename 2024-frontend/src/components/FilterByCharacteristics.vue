<script setup>
import { ref, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import { getCharacteristicsOptions } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const economicModel = computed(() => storeFilters.getParam("economicModel"))
const managementType = computed(() => storeFilters.getParam("managementType"))
const productionType = computed(() => storeFilters.getParam("productionType"))
const options = ref(getCharacteristicsOptions())
const storeFilters = useStoreFilters()
</script>

<template>
  <FilterByBase label="Caractéristiques">
    <DsfrCheckboxSet
      legend="Types d’établissement :"
      :modelValue="economicModel"
      @update:modelValue="storeFilters.set('economicModel', $event)"
      :options="options.economicModel"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Modes de gestion :"
      :modelValue="managementType"
      @update:modelValue="storeFilters.set('managementType', $event)"
      :options="options.managementType"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Modes de production :"
      :modelValue="productionType"
      @update:modelValue="storeFilters.set('productionType', $event)"
      :options="options.productionType"
      small
      inline
    />
  </FilterByBase>
</template>
