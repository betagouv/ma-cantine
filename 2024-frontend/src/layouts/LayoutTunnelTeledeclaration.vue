<script setup>
import { computed } from "vue"
import { useRouter, useRoute } from "vue-router"

const router = useRouter()
const route = useRoute()
const previousStep = computed(() => route.meta.previous)
const nextStep = computed(() => route.meta.next)

const goPrev = () => { router.push({ name: previousStep.value }) }
const goNext = () => { router.push({ name: nextStep.value }) }
const exit = () => { router.push({ name: "GestionnaireCantineTeledeclarationEnCours" })}
</script>
<template>
  <div class="layout-tunnel-teledeclaration ma-cantine--sticky__container">
    <nav class="layout-tunnel-teledeclaration__top-bar ma-cantine--sticky__top fr-background-default--grey ma-cantine--flex-between ma-cantine--flex-gap-1 fr-py-2w">
      <DsfrButton
        tertiary
        icon="fr-icon-logout-box-r-line"
        label="Sauvegarder et quitter"
        @click="exit"
      />
      <div>
        <DsfrButton
          secondary
          icon="fr-icon-arrow-left-s-first-line"
          label="Etape précédente"
          @click="goPrev"
          :disabled="!previousStep"
          class="fr-mr-2w"
        />
        <DsfrButton
          secondary
          icon="fr-icon-arrow-right-s-last-line"
          label="Etape suivante"
          @click="goNext"
          :disabled="!nextStep"
        />
      </div>
    </nav>
    <div class="layout-tunnel-teledeclaration__content fr-grid-row fr-grid-row--gutters">
      <div class="layout-tunnel-teledeclaration__sidebar fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
        <p>Sidebar Tunnel</p>
      </div>
      <div class="fr-col-12 fr-col-md-9">
        <RouterView />
      </div>
    </div>
  </div>
</template>
