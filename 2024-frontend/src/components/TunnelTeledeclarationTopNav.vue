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
  <nav class="tunnel-teledeclaration-top-nav fr-background-default--grey fr-py-2w">
    <div class="ma-cantine--z-index-1 ma-cantine--flex-between ma-cantine--flex-gap-1">
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
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-top-nav {
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
</style>
