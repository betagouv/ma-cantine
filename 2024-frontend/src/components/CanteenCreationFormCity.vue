<script setup>
import { reactive, ref } from "vue"
const citySelected = ref([])
const citiesOptions = reactive([
  {
    id: "0",
    citycode: "73065",
    city: "Chambéry",
  },
  {
    id: "1",
    citycode: "73065-2",
    city: "Chambéry 2",
  },
])
</script>

<template>
  <DsfrMultiselect
    v-model="citySelected"
    label="Ville *"
    labelVisible
    :options="citiesOptions"
    label-key="city"
    search
    :filtering-keys="['city']"
  >
    <template #no-results>
      Tapez les 3 premières lettres de votre ville
    </template>
  </DsfrMultiselect>
</template>
