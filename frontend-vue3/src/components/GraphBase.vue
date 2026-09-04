<script setup>
import { computed, ref } from "vue"
const props = defineProps(["valuesToVerify", "description"])

const accordion = ref()
const displayGraph = computed(() => {
  const incorrectValues = props.valuesToVerify.filter(
    (value) => value === null || value === undefined || value === false
  )
  return incorrectValues.length === 0
})
</script>
<template>
  <slot v-if="displayGraph"></slot>
  <p v-else>
    Une erreur est survenue lors de l'affichage du graphique, veuillez recharger la page et si l'erreur persiste
    contactez-nous.
  </p>
  <DsfrAccordionsGroup v-if="description && displayGraph" v-model="accordion">
    <DsfrAccordion title="Description du graphique" titleTag="p">
      <p class="fr-mb-0">{{ description }}</p>
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>
