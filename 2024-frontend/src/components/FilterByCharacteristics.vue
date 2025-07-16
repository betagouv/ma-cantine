<script setup>
import { ref } from "vue"
import { getCharacteristicsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

const economicModel = ref([])
const managementType = ref([])
const productionType = ref([])
const options = ref(getCharacteristicsOptions())
</script>

<template>
  <AppDropdown label="Caractéristiques">
    <DsfrCheckboxSet
      legend="Types d’établissement :"
      :modelValue="economicModel"
      :options="options.economicModel"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Modes de gestion :"
      :modelValue="managementType"
      :options="options.managementType"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Modes de production :"
      :modelValue="productionType"
      :options="options.productionType"
      small
      inline
    />
  </AppDropdown>
</template>
