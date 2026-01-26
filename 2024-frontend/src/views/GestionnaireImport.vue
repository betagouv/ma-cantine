<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const pages = ref([
  {
    title: "Importer des cantines",
    to: { name: "GestionnaireImportCantines" },
    description: "Vous voulez créer ou mettre à jour des cantines."
  },
  {
    title: "Importer des achats",
    to: { name: "GestionnaireImportAchats" },
    description: "Vous voulez importer des données d'achat pour des cantines existantes.",
  },
  {
    title: "Importer des bilans simples",
    to: { name: "GestionnaireImportBilansSimples" },
    description: "Vous voulez importer des bilans simples pour des cantines existantes.",
  },
  {
    title: "Importer des bilans détaillés",
    disabled: true,
    description: "Cette fonctionnalité est en cours de construction et sera disponible prochainement.",
    badges: [
      {
        label: "Bientôt disponible",
        type: "warning",
        noIcon: false,
      },
    ],
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
  <section>
    <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters">
      <li v-for="page in pages" :key="page.name" class="fr-col-12 fr-col-md-4">
        <DsfrCard :title="page.title" :link="page.to" :description="page.description">
          <template #start-details v-if="page.badges">
            <DsfrBadge
              v-for="badge in page.badges"
              :key="badge"
              :label="badge.label"
              :type="badge.type || 'info'"
              class="fr-mr-1v"
              :no-icon="badge.noIcon"
            />
          </template>
        </DsfrCard>
      </li>
    </ul>
  </section>
</template>
