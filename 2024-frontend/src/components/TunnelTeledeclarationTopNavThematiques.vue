<script setup>
import { computed } from "vue"
import { useRouter, useRoute } from "vue-router"

const emit = defineEmits(["save", "quit"])
const router = useRouter()
const route = useRoute()
const previousStep = computed(() => route.meta.previous)
const nextStep = computed(() => route.meta.next)
const isLast = computed(() => route.meta.isLast)

const goToPrevious = () => router.push({ name: previousStep.value })
const saveAndGoNext = () => {
  if (isLast.value) emit("save", "GestionnaireCantineTeledeclarationEnCours")
  else emit("save", nextStep.value)
}
</script>

<template>
  <nav class="tunnel-teledeclaration-top-nav-thematiques ma-cantine--sticky__top fr-background-default--grey fr-py-2w">
    <DsfrButton
      tertiary
      icon="fr-icon-close-line"
      label="Quitter sans enregistrer"
      @click="emit('quit', 'GestionnaireCantineTeledeclarationEnCours')"
    />
    <DsfrButton
      v-if="previousStep"
      secondary
      icon="fr-icon-arrow-left-s-first-line"
      label="Revenir au volet précédent"
      @click="goToPrevious()"
    />
    <DsfrButton
      icon="fr-icon-arrow-right-line"
      :icon-right="true"
      :label="isLast ? 'Enregistrer et aller à ma télédéclaration' : 'Enregistrer et passer au volet suivant'"
      @click="saveAndGoNext()"
    />
  </nav>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-top-nav-thematiques {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}
</style>
