<script setup>
import { ref, useTemplateRef } from "vue"
import { onClickOutside } from "@vueuse/core"
import openDataService from "@/services/openData.js"

defineProps(["errorRequired"])
const emit = defineEmits(["select"])

/* Search */
const search = ref()
const noResults = ref()
const findCities = () => {
  emit("select", {})
  const trimSearch = search.value.trim()
  if (trimSearch.length < 3) return
  openDataService
    .findCities(trimSearch)
    .then((response) => {
      if (response.features.length > 0) displayOptions(response.features)
      else displayError(trimSearch)
    })
    .catch((e) => {
      console.log("error", e)
    })
}

const displayError = (name) => {
  noResults.value = `Aucune commune trouvée pour « ${name} »`
  expanded.value = false
}

/* List of options */
const expanded = ref(false)
const citiesOption = ref([])
const dropdown = useTemplateRef("dropdown")
const displayOptions = (options) => {
  noResults.value = false
  expanded.value = true
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
const closeDropdown = () => {
  expanded.value = false
  if (!citySelected.value) search.value = ""
}
onClickOutside(dropdown, closeDropdown)

/* Selection */
const citySelected = ref()
const selectCity = () => {
  const { city, cityInseeCode, postalCode, department } = citiesOption.value[citySelected.value]
  emit("select", { city, cityInseeCode, postalCode, department })
  citiesOption.value = []
  search.value = city
  citySelected.value = null
  expanded.value = false
}
</script>

<template>
  <div class="canteen-creation-city fr-select-group">
    <div class="canteen-creation-city__input fr-multi-select">
      <DsfrInputGroup
        label="Ville *"
        label-visible
        v-model="search"
        placeholder="Tapez les 3 premières lettre de votre ville"
        @update:modelValue="findCities()"
        :error-message="noResults || errorRequired"
      />
    </div>
    <DsfrRadioButtonSet
      v-if="citiesOption.length > 0"
      ref="dropdown"
      hint="Sélectionnez une commune parmis la liste"
      class="canteen-creation-city__options fr-multiselect__collapse fr-collapse"
      :class="{
        'fr-collapse--expanded': expanded,
      }"
      v-model="citySelected"
      :options="citiesOption"
      @update:modelValue="selectCity()"
      small
    />
  </div>
</template>

<style lang="scss">
.canteen-creation-city {
  &__input {
    .fr-input-group {
      margin-bottom: 0.25rem !important;
    }
  }

  &__options {
    width: 100% !important;
  }
}
</style>
