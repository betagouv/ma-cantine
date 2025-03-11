<script setup>
import { ref } from "vue"
import openDataService from "@/services/openData.js"

defineProps(["errorMessage"])

const search = ref()
const citySelected = ref()
const citiesOption = ref([])
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

const displayOptions = (options) => {
  noResults.value = false
  const cleanedOptions = options.map((option) => {
    return {
      label: option.properties.label,
      value: option.properties.citycode,
    }
  })
  citiesOption.value = cleanedOptions
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
    small
  />
</template>
