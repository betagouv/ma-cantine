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
      if (response instanceof Error) throw Error()
      else success()
    })
    .catch(() => {
      loading.value = true
      error.value = true
    })
}
const success = async () => {
  const satelliteInfos = await canteensService.fetchCanteen(props.satId)
  emit("satelliteAdded", satelliteInfos)
}
</script>

<template>
  <div v-if="error" class="fr-error-text">Une erreur est survenue lors de l'ajout du restaurant satellite à votre groupe, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr</div>
  <DsfrButton v-else secondary :label="label" @click="addSatellite()" :disabled="loading" />
</template>
