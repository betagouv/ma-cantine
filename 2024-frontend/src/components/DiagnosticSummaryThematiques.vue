<script setup>
import { computed } from "vue"
import diagnosticsMacaron from "@/services/diagnosticsMacaron.js"

const props = defineProps(["diagnosticRecap", "voletKey"])

const objectiveReachedSentences = {
  information: "La cantine informe ses convives de toutes ses démarches pour du mieux manger.",
  gaspillage: "La cantine est engagée dans une démarche de réduction drastique de son gaspillage.",
  diversification: "La cantine est en conformité avec le volet diversification des sources de protéines et menus végétariens.",
  plastique: "La cantine n’utilise plus du tout de plastique ni pour sa production ni pour le service.",
}

const sentence = computed(() => {
  const isReached = diagnosticsMacaron.isObjectiveReached(props.voletKey, props.diagnosticRecap)
  if (isReached) return objectiveReachedSentences[props.voletKey]
  return "Cet établissement ne respecte pas encore la loi EGalim pour cette mesure."
})
</script>
<template>
  <p class="fr-mb-0">{{ sentence }}</p>
</template>
