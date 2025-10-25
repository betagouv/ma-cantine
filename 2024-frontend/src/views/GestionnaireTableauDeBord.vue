<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import GestionnaireGuides from "@/components/GestionnaireGuides.vue"

const store = useRootStore()

const canteenSentence = computed(() => {
  const count = store.canteenPreviews.length
  if (count === 0) return "vous n'avez pas encore de cantine"
  else if (count === 1) return "1 cantine"
  return `${count} cantines`
})

const pictoDocuments = "/static/images/picto-dsfr/documents.svg"
const pictoDocumentAdd = "/static/images/picto-dsfr/document-add.svg"
</script>

<template>
  <section>
    <h1>Bienvenue dans votre espace, {{ store.loggedUser.firstName }}</h1>
    <p class="fr-text--lead">{{ canteenSentence }}</p>
  </section>
  <section>
    <ul
      v-if="store.canteenPreviews.length === 0"
      class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters fr-my-4w"
    >
      <li class="fr-col-12 fr-col-md-6">
        <DsfrCard
          class="gestionnaire-tableau-de-bord__card"
          title="Ajouter une cantine via le formulaire"
          :imgSrc="pictoDocuments"
          :link="{ name: 'GestionnaireCantineAjouter' }"
          endDetail="Ajouter votre cantine"
          description="Pour ajouter votre lieu de restauration collective munissez-vous de votre numéro SIRET ou du numéro SIREN de votre unité légale."
        />
      </li>
      <li class="fr-col-12 fr-col-md-6">
        <DsfrCard
          class="gestionnaire-tableau-de-bord__card"
          title="Créer plus de 5 cantines via import de fichier"
          :imgSrc="pictoDocumentAdd"
          :link="{ name: 'GestionnaireImportCantines' }"
          endDetail="Importer toutes vos cantines"
          description="Notre outil d’import de masse vous permet de créer vos cantines ou de modifier vos cantines existantes d’un coup. Il concerne uniquement les gestionnaires qui ont plus de 5 cantines."
        />
      </li>
    </ul>
  </section>
  <section class="ma-cantine--stick-to-footer">
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
