<script setup>
import { computed, ref, useId } from "vue"
const props = defineProps(["valuesToVerify", "description"])

const displayOptionName = useId()
const displayOption = ref("graph")
const displayGraph = computed(() => {
  const incorrectValues = props.valuesToVerify.filter(
    (value) => value === null || value === undefined || value === false
  )
  return incorrectValues.length === 0
})
</script>
<template>
  <template v-if="displayGraph">
    <DsfrSegmentedSet
      v-if="description"
      :name="displayOptionName"
      label="Choix d'affichage"
      :options="[
        {
          label: 'Graphique',
          value: 'graph',
        },
        {
          label: 'Texte',
          value: 'text',
        },
      ]"
      v-model="displayOption"
      small
      class="fr-mb-2w"
    />
    <p v-if="displayOption === 'text'" class="fr-mb-0">{{ description || "Aucune description" }}</p>
    <slot v-else></slot>
  </template>
  <p v-else>
    Une erreur est survenue lors de l'affichage du graphique, veuillez recharger la page et si l'erreur persiste
    contactez-nous.
  </p>
</template>
