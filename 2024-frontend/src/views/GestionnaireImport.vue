<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"

/* Pages */
const staffPages = [
{
    title: "Ajouter des gestionnaires",
    to: { name: "GestionnaireImportCantinesGestionnaires" },
    description: "Vous voulez ajouter des gestionnaires en masse via le SIRET des cantines sans envoyer d'invitation email.",
    detail: "Réservé aux utilisateurs administrateurs",
  },
]
const commonPages = [
  {
    title: "Créer des cantines",
    to: { name: "GestionnaireImportCantinesCreer" },
    description: "Vous voulez créer des cantines en masse à partir de leur numéro SIRET.",
  },
  {
    title: "Modifier des cantines",
    to: { name: "GestionnaireImportCantinesCreer" },
    description: "Vous voulez modifier des cantines dont vous êtes gestionnaire.",
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
    title: "Importer des bilans simples via ID",
    to: { name: "GestionnaireImportBilansSimples" },
    detail: "Pour toutes les cantines",
    description: "Vous voulez importer des bilans simples pour des cantines, des groupes de restaurants satellites ou des cantines rattachées à une unité légale.",
    badges: [
      {
        label: "Nouveauté",
        noIcon: false,
        type: "new",
      }
    ],
  },
  {
    title: "Importer des bilans simples via SIRET",
    to: { name: "GestionnaireImportBilansSimplesSIRET" },
    description: "Vous voulez importer des bilans simples pour des cantines existantes.",
    detail: "Pour les cantines inscrites avec SIRET",
  },
  {
    title: "Importer des bilans détaillés",
    to: { name: "GestionnaireImportBilansDetailles" },
    description: "Vous voulez importer des bilans détaillés pour des cantines existantes.",
  },
]

/* Data */
const route = useRoute()
const store = useRootStore()
const pages = computed(() =>  store.loggedUser.isStaff ? [...staffPages, ...commonPages] : commonPages)
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
