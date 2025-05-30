<script setup>
import { useRoute } from "vue-router"
const route = useRoute()

const scrollTop = () => {
  window.scrollTo(0, 0)
}
</script>

<template>
  <div class="layout-one-column">
    <h1 class="fr-my-8w">{{ route.meta.title }}</h1>
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-lg-7">
        <slot></slot>
      </div>
      <div
        class="ma-cantine--sticky__container fr-hidden fr-unhidden-lg fr-col-lg-5 fr-grid-row fr-grid-row--top fr-grid-row--right"
      >
        <DsfrButton
          class="ma-cantine--sticky__bottom"
          label="Retour en haut de page"
          icon="fr-icon-arrow-up-line"
          secondary
          @click="scrollTop"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.layout-one-column {
  section {
    margin-top: 2rem;
  }
}
</style>
