<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import GestionnairesGuides from "@/components/GestionnairesGuides.vue"

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
  <section>
    <GestionnairesGuides />
  </section>
</template>
