<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const pages = ref([
  {
    title: "Importer des cantines",
    to: { name: "GestionnaireImportCantines" },
    description: "Vous voulez créer ou mettre à jour des cantines.",
  },
  {
    title: "Importer des achats via ID",
    to: { name: "GestionnaireImportAchats" },
    description: "Vous voulez importer des données d'achat pour des groupes de restaurants satellites ou des cantines rattachées à une unité légale.",
    detail: "Pour toutes les cantines",
    badges: [
      {
        label: "Nouveauté",
        noIcon: false,
        type: "new",
      }
    ],
  },
  {
    title: "Importer des achats",
    to: { name: "GestionnaireImportAchatsSIRET" },
    description: "Vous voulez importer des données d'achat pour des cantines existantes.",
    detail: "Pour les cantines inscrites avec SIRET",
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
  <section class="gestionnaire-import fr-col-12 fr-col-md-7">
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
        <DsfrCard
          class="gestionnaire-import__card"
          :title="page.title"
          :link="page.to"
          :description="page.description"
          :endDetail="page.detail"
          :badges="page.badges"
        />
      </li>
    </ul>
  </section>
</template>

<style lang="scss">
.gestionnaire-import {
  &__card {
    .fr-card__content {
      padding-top: 3rem;
    }
  }
}
</style>
