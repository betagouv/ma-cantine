<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const tiles = ref([
  {
    title: "Importer des cantines",
    name: "GestionnaireImportCantines",
    description: "Vous voulez créer ou mettre à jour des cantines.",
    tags: ["Excel", "CSV"],
  },
  {
    title: "Importer des achats",
    name: "GestionnaireImportAchats",
    description: "Vous voulez importer des données d'achat pour des cantines existantes.",
    tags: ["CSV"],
  },
])
</script>

<template>
  <section class="fr-col-12 fr-col-md-7">
    <h1>{{ route.meta.title }}</h1>
    <p>
      Gagnez du temps en important vos données directement dans
      <em>ma cantine.</em>
      <br />
      Pour une expérience optimale, veuillez bien respecter les formats attendus.
    </p>
  </section>
  <section></section>
</template>
