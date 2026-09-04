<script setup>
import { ref } from "vue"
import canteensService from "@/services/canteens"

const props = defineProps(["satId", "groupId"])
const emit = defineEmits(["satelliteAdded"])
const loading = ref(false)
const error = ref(false)

/* Add Satellite */
const label = ref("Ajouter ce restaurant satellite à mon groupe")
const addSatellite = () => {
  loading.value = true
  error.value = false
  label.value = "Ajout en cours..."
  canteensService
    .linkSatellite(props.groupId, props.satId)
    .then((response) => {
      if (response.status === "error") displayError(response)
      else emit("satelliteAdded")
    })
    .catch(displayError)
}

const displayError = (serverError) => {
  loading.value = true
  error.value = serverError.message
}
</script>

<template>
  <div v-if="error" class="fr-error-text">{{ error }}</div>
  <DsfrButton v-else secondary :label="label" @click="addSatellite()" :disabled="loading" />
</template>
