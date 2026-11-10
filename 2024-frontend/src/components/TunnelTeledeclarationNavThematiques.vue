<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

const emit = defineEmits(["save"])
const route = useRoute()
const nextStep = computed(() => route.meta.next)
const isLast = computed(() => route.meta.isLast)

const saveAndGoNext = () => {
  if (isLast.value) emit("save", { page: "GestionnaireCantineTeledeclarationEnCours", checkErrors: true })
  else emit("save", { page: nextStep.value, checkErrors: true })
}
</script>

<template>
  <nav class="tunnel-teledeclaration-nav-thematiques ma-cantine--sticky__top fr-background-default--grey fr-py-2w">
    <DsfrButton
      tertiary
      no-outline
      icon="fr-icon-save-line"
      label="Enregistrer et quitter"
      @click="emit('save', { page: 'GestionnaireCantineTeledeclarationEnCours', checkErrors: false })"
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
.tunnel-teledeclaration-nav-thematiques {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}
</style>
