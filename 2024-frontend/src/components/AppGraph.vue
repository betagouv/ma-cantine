<script setup>
import { computed } from "vue"
const props = defineProps(["valuesToVerify", "description"])

const displayGraph = computed(() => {
  const incorrectValues = props.valuesToVerify.filter(
    (value) => value === null || value === undefined || value === false
  )
  return incorrectValues.length === 0
})
</script>
<template>
  <div>
    <slot v-if="displayGraph"></slot>
    <p v-else>
      Une erreur est survenue lors de l'affichage du graphique, veuillez recharger la page et si l'erreur persiste
      contactez-nous.
    </p>
    <DsfrAccordion v-if="description" title="Description du graphique" titleTag="p">
      <p class="fr-mb-0">{{ description }}</p>
    </DsfrAccordion>
  </div>
</template>
