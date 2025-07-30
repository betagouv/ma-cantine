<script setup>
import { computed } from "vue"
const props = defineProps(["error"])

const description = computed(() => {
  if (props.error === "noYear") return "vous devez sélectionner une année"
  if (props.error === "noFilter") return "aucun filtre sélectionné"
  return "veuillez recharger la page pour renouveller votre recherche, si l'erreur persiste contactez-nous."
})
</script>
<template>
  <DsfrNotice type="alert" title="Une erreur est survenue lors de l'affichage des résultats :" :desc="description" />
</template>
