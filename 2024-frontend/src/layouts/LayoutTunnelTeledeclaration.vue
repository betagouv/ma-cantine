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
  <div class="layout-tunnel-teledeclaration ma-cantine--sticky__container ma-cantine--stick-to-footer">
    <nav class="layout-tunnel-teledeclaration__top-bar ma-cantine--sticky__top fr-background-default--grey fr-py-2w">
      <div class="ma-cantine--z-index-1 ma-cantine--flex-between ma-cantine--flex-gap-1 ">
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
      </div>
    </nav>
    <div class="layout-tunnel-teledeclaration__content fr-grid-row">
      <div class="layout-tunnel-teledeclaration__sidebar fr-background-alt--blue-france fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
        <div class="ma-cantine--z-index-1">
          <p>Sidebar Tunnel</p>
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-9 fr-pl-0 fr-pl-md-2w">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.layout-tunnel-teledeclaration {
  &__top-bar {
    &:before {
      content: "";
      position: absolute;
      top: 0;
      left: 50%;
      width: 100vw;
      height: 100%;
      background-color: inherit;
      transform: translateX(-50%);
      z-index: 0;
    }
  }

  &__sidebar {
    position: relative;

    &:before {
      content: "";
      position: absolute;
      top: 0;
      right: 0;
      width: 100vw;
      height: 100%;
      background-color: inherit;
    }
  }
}
</style>
