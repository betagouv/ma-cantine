<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

const emit = defineEmits(["save"])
const route = useRoute()
const previousStep = computed(() => route.meta.previous)
const nextStep = computed(() => route.meta.next)
</script>

<template>
  <nav class="tunnel-teledeclaration-nav-approvisionnements ma-cantine--sticky__top fr-background-default--grey fr-py-2w">
    <DsfrButton
      tertiary
      icon="fr-icon-save-line"
      label="Enregistrer et finir plus tard"
      no-outline
      @click="emit('save', { page: 'GestionnaireCantineTeledeclarationEnCours', checkErrors: false })"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-left-s-first-line"
      label="Étape précédente"
      @click="emit('save', { page: previousStep, checkErrors: true })"
      :disabled="!previousStep"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-right-s-last-line"
      label="Étape suivante"
      @click="emit('save', { page: nextStep, checkErrors: true })"
      :disabled="!nextStep"
      :icon-right="true"
    />
  </nav>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-nav-approvisionnements {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}
</style>
