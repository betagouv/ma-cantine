<script setup>
import { ref } from "vue"
import openDataService from "@/services/openData.js"

defineProps(["errorMessage"])
const emit = defineEmits(["select"])

/* Search */
const search = ref()
const noResults = ref()
const findCities = () => {
  const trimSearch = search.value.trim()
  if (trimSearch.length < 3) return
  openDataService
    .findCities(trimSearch)
    .then((response) => {
      if (response.features.length > 0) displayOptions(response.features)
      else noResults.value = `Aucune commune trouvée pour « ${trimSearch} »`
    })
    .catch((e) => {
      console.log("error", e)
    })
}

/* List of options */
const citiesOption = ref([])
const displayOptions = (options) => {
  noResults.value = false
  const cleanedOptions = options.map((option, index) => {
    return {
      value: index,
      label: option.properties.label,
      city: option.properties.label, // Needed for CanteenCreationForm emit
      cityInseeCode: option.properties.citycode, // Needed for CanteenCreationForm emit
      postalCode: option.properties.postcode, // Needed for CanteenCreationForm emit
      department: option.properties.citycode.slice(0, 2), // Needed for CanteenCreationForm emit
    }
  })
  citiesOption.value = cleanedOptions
}

/* Selection */
const citySelected = ref()
const selectCity = () => {
  const { city, cityInseeCode, postalCode, department } = citiesOption.value[citySelected.value]
  emit("select", { city, cityInseeCode, postalCode, department })
  citiesOption.value = []
  search.value = city
  citySelected.value = null
}
</script>

<template>
  <DsfrInputGroup
    label="Ville *"
    label-visible
    v-model="search"
    placeholder="Tapez les 3 premières lettre de votre ville"
    @update:modelValue="findCities()"
    :error-message="noResults"
  />
  <DsfrRadioButtonSet
    v-if="citiesOption.length > 0"
    legend="Sélectionnez une commune parmis la liste"
    v-model="citySelected"
    :options="citiesOption"
    @update:modelValue="selectCity()"
    small
  />
</template>
