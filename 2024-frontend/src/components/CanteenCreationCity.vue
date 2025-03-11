<script setup>
import { ref } from "vue"
import openDataService from "@/services/openData.js"

defineProps(["errorMessage"])
const emit = defineEmits(["select"])

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
  const cleanedOptions = options.map((option, index) => {
    return {
      value: index,
      label: option.properties.label,
      cityInseeCode: option.properties.citycode,
      postalCode: option.properties.postcode,
      department: option.properties.citycode.slice(0, 2),
    }
  })
  citiesOption.value = cleanedOptions
}

const selectCity = () => {
  const optionSelected = citiesOption.value[citySelected.value]
  emit("select", {
    postalCode: optionSelected.postalCode,
    city: optionSelected.label,
    cityInseeCode: optionSelected.cityInseeCode,
    department: optionSelected.department,
  })
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
