<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import { useStoreFilters } from "@/stores/filters"
import { getCharacteristicsOptions } from "@/services/filters"
import FilterByBase from "@/components/FilterByBase.vue"

const economicModel = computed(() => storeFilters.getParam("economicModel"))
const managementType = computed(() => storeFilters.getParam("managementType"))
const productionType = computed(() => storeFilters.getParam("productionType"))
const options = ref(getCharacteristicsOptions())
const storeFilters = useStoreFilters()
const route = useRoute()

/* Prefill filters from query */
const query = route.query
if (query.economicModel) storeFilters.setFromQuery("economicModel", query.economicModel, options.value.economicModel)
if (query.managementType)
  storeFilters.setFromQuery("managementType", query.managementType, options.value.managementType)
if (query.productionType)
  storeFilters.setFromQuery("productionType", query.productionType, options.value.productionType)
</script>

<template>
  <FilterByBase label="Caractéristiques">
    <DsfrCheckboxSet
      legend="Modèle économique"
      :modelValue="economicModel"
      @update:modelValue="storeFilters.set('economicModel', $event)"
      :options="options.economicModel"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Mode de gestion"
      :modelValue="managementType"
      @update:modelValue="storeFilters.set('managementType', $event)"
      :options="options.managementType"
      small
      inline
    />
    <DsfrCheckboxSet
      legend="Mode de production"
      :modelValue="productionType"
      @update:modelValue="storeFilters.set('productionType', $event)"
      :options="options.productionType"
      small
      inline
    />
  </FilterByBase>
</template>
