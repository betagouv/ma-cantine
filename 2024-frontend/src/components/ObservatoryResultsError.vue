<script setup>
import { computed } from "vue"
const props = defineProps(["code"])

const description = computed(() => {
  if (props.code === "noYear") return "vous devez sélectionner une année"
  if (props.code === "noFilter") return "aucun filtre sélectionné"
  return "veuillez recharger la page pour renouveller votre recherche, si l'erreur persiste contactez-nous."
})
</script>
<template>
  <DsfrNotice type="alert" title="Une erreur est survenue lors de l'affichage des résultats :" :desc="description" />
</template>
