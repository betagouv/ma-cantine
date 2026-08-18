<script setup>
import { computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const router = useRouter()
const route = useRoute()
const previousStep = computed(() => route.meta.previous)
const nextStep = computed(() => route.meta.next)

const goPrev = () => { router.push({ name: previousStep.value }) }
const goNext = () => { router.push({ name: nextStep.value }) }
</script>

<template>
  <nav class="tunnel-teledeclaration-top-nav fr-background-default--grey fr-py-2w">
    <AppLinkRouter
      :to="{ name: 'GestionnaireCantineTeledeclarationEnCours' }"
      title="Enregistrer et finir plus tard"
      :hide-arrow-icon="true"
      icon="fr-icon-save-line"
      class="fr-mr-2w"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-left-s-first-line"
      label="Étape précédente"
      @click="goPrev"
      :disabled="!previousStep"
      class="fr-mr-2w"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-right-s-last-line"
      label="Étape suivante"
      @click="goNext"
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
