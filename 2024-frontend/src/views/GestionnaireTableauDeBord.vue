<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import GestionnaireGuides from "@/components/GestionnaireGuides.vue"
import GestionnaireCanteensCreate from "@/components/GestionnaireCanteensCreate.vue"

const store = useRootStore()

const canteenSentence = computed(() => {
  const count = store.canteenPreviews.length
  if (count === 0) return "vous n'avez pas encore de cantine"
  else if (count === 1) return "1 cantine"
  return `${count} cantines`
})
</script>

<template>
  <section>
    <h1>Bienvenue dans votre espace, {{ store.loggedUser.firstName }}</h1>
    <p class="fr-text--lead">{{ canteenSentence }}</p>
  </section>
  <section class="ma-cantine--stick-to-footer">
    <GestionnaireCanteensCreate v-if="store.canteenPreviews.length === 0" />
    <GestionnaireGuides />
  </section>
</template>

<style lang="scss">
.gestionnaire-tableau-de-bord {
  &__card {
    .fr-card__header {
      padding-top: 1rem !important;
    }

    .fr-card__img img {
      max-height: 7rem !important;
      object-fit: contain !important;
    }
  }
}
</style>
