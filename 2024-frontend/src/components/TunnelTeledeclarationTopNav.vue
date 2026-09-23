<script setup>
import { computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"

const emit = defineEmits(["save"])
const router = useRouter()
const route = useRoute()
const teledeclarationStore = useStoreTeledeclaration()
const previousStep = computed(() => route.meta.previous)
const nextStep = computed(() => route.meta.next)

const saveAndQuit = async () => {
  await teledeclarationStore.saveDiagnostic()
  router.push({ name: 'GestionnaireCantineTeledeclarationEnCours' })
}
</script>

<template>
  <nav class="tunnel-teledeclaration-top-nav ma-cantine--sticky__top fr-background-default--grey fr-py-2w">
    <DsfrButton
      tertiary
      icon="fr-icon-save-line"
      label="Enregistrer et finir plus tard"
      no-outline
      @click="saveAndQuit()"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-left-s-first-line"
      label="Étape précédente"
      @click="emit('save', previousStep)"
      :disabled="!previousStep"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-right-s-last-line"
      label="Étape suivante"
      @click="emit('save', nextStep)"
      :disabled="!nextStep"
      :icon-right="true"
    />
  </nav>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-top-nav {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}
</style>
