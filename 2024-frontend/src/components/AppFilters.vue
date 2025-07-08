<script setup>
import { ref } from "vue"
import { getYearsOptions, getCharacteristicsOptions } from "@/services/filters"
import AppDropdown from "@/components/AppDropdown.vue"

/* Display */
const props = defineProps(["filters"])
const displayYearFilter = ref(props.filters.includes("years"))
const displayCharacteristicsFilter = ref(props.filters.includes("characteristics"))

/* Otions */
const yearsOptions = ref(getYearsOptions())
const characteristicsOptions = ref(getCharacteristicsOptions())

/* Models */
const yearModel = ref("")
const economicModel = ref("")
const managementType = ref("")
const productionType = ref([])
</script>

<template>
  <ul class="ma-cantine--unstyled-list">
    <li v-if="displayCharacteristicsFilter">
      <AppDropdown label="Caractéristiques">
        <DsfrRadioButtonSet
          legend="Type d’établissement"
          :modelValue="economicModel"
          :options="characteristicsOptions.economicModel"
          small
          inline
        />
        <DsfrRadioButtonSet
          legend="Mode de gestion"
          :modelValue="managementType"
          :options="characteristicsOptions.managementType"
          small
          inline
        />
        <DsfrCheckboxSet
          legend="Modes de production"
          :modelValue="productionType"
          :options="characteristicsOptions.productionType"
          small
        />
      </AppDropdown>
    </li>
    <li v-if="displayYearFilter">
      <AppDropdown label="Années">
        <DsfrRadioButtonSet :modelValue="yearModel" :options="yearsOptions" small />
      </AppDropdown>
    </li>
  </ul>
</template>
