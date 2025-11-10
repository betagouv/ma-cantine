<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const pages = ref([
  {
    title: "Importer des cantines",
    to: { name: "GestionnaireImportCantines" },
    description: "Vous voulez créer ou mettre à jour des cantines.",
    badges: ["Excel", "CSV"],
  },
  {
    title: "Importer des achats",
    to: { name: "GestionnaireImportAchats" },
    description: "Vous voulez importer des données d'achat pour des cantines existantes.",
    badges: ["CSV"],
  },
  {
    title: "Importer des bilans",
    disabled: true,
    description: "Cette fonctionnalité est en cours de construction et sera disponible prochainement.",
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
    <ul class="ma-cantine--unstyled-list">
      <li v-for="page in pages" :key="page.name" class="fr-mb-1w">
        <DsfrCard :title="page.title" :link="page.to" :description="page.description" :horizontal="true">
          <template #start-details v-if="page.badges">
            <DsfrBadge v-for="badge in page.badges" :key="badge" :label="badge" class="fr-mr-1v" no-icon />
          </template>
        </DsfrCard>
      </li>
    </ul>
  </section>
</template>
