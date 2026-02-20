<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"

/* Pages */
const staffPages = [
{
    title: "Ajouter des gestionnaires aux cantines",
    to: { name: "GestionnaireImportCantinesGestionnaires" },
    description: "Pour ajouter des gestionnaires à des cantines sans envoyer d'invitation email.",
    detail: "Pour les utilisateurs administrateurs seulement",
    badges: [
      {
        label: "SIRET",
        noIcon: true,
        type: "info",
      }
    ],
  },
]
const commonPages = [
  {
    title: "Créer des cantines",
    to: { name: "GestionnaireImportCantinesCreer" },
    description: "Pour créer des cantines en masse avec un numéro SIRET.",
    badges: [
      {
        label: "SIRET",
        noIcon: true,
        type: "info",
      }
    ],
  },
  {
    title: "Modifier des cantines",
    to: { name: "GestionnaireImportCantinesModifier" },
    description: "Pour mettre à jour les informations des cantines dont vous êtes gestionnaire. Pour les cantines inscrites avec SIRET ou rattachées à une unité légale.",
    detail: "Cet import n'est pas utilisable pour les groupes de restaurants satellites",
    badges: [
      {
        label: "ID",
        noIcon: true,
        type: "info",
      }
    ],
  },
  {
    title: "Ajouter des achats",
    to: { name: "GestionnaireImportAchats" },
    description: "Pour ajouter des achats à des cantines dont vous êtes gestionnaire.",
    detail: "Pour les cantines et les groupes de restaurants satellites",
    badges: [
      {
        label: "ID",
        noIcon: true,
        type: "info",
      }
    ],
  },
  {
    title: "Ajouter des achats via le SIRET de la cantine",
    to: { name: "GestionnaireImportAchatsSIRET" },
    description: "Pour ajouter des achat à des cantines dont vous êtes gestionnaire inscrite avec un numéro SIRET.",
    badges: [
      {
        label: "SIRET",
        noIcon: true,
        type: "info",
      }
    ],
  },
  {
    title: "Créer ou modifier des bilans simples",
    to: { name: "GestionnaireImportBilansSimples" },
    description: "Pour créer ou modifier des bilans simples pour des cantines, des groupes de restaurants satellites ou des cantines rattachées à une unité légale.",
    detail: "Pour les cantines et les groupes de restaurants satellites",
    badges: [
      {
        label: "ID",
        noIcon: true,
        type: "info",
      }
    ],
  },
  {
    title: "Créer ou modifier des bilans simples via le SIRET de la cantine",
    to: { name: "GestionnaireImportBilansSimplesSIRET" },
    description: "Pour créer ou modifier des bilans simples pour des cantines dont vous êtes gestionnaire inscrite avec un numéro SIRET.",
    badges: [
      {
        label: "SIRET",
        noIcon: true,
        type: "info",
      }
    ],
  },
  {
    title: "Créer ou modifier des bilans détaillés via le SIRET de la cantine",
    to: { name: "GestionnaireImportBilansDetailles" },
    description: "Pour créer ou modifier des bilans détaillés pour des cantines dont vous êtes gestionnaire inscrite avec un numéro SIRET.",
    badges: [
      {
        label: "SIRET",
        noIcon: true,
        type: "info",
      }
    ],
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
