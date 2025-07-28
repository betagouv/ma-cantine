<script setup>
import { useRoute } from "vue-router"

const route = useRoute()
const pictoDataVisualization = "/static/images/picto-dsfr/data-visualization.svg"
const pictoDocuments = "/static/images/picto-dsfr/documents.svg"
const documentRapport = "/static/documents/Rapport_Bilan_Statistique_EGALIM_2024.pdf"
</script>

<template>
  <section class="fr-grid-row fr-grid-row--gutters fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-lg-6">
      <h1>{{ route.meta.title }}</h1>
      <p>
        La loi EGalim, complétée par la loi Climat et Résilience, a défini des obligations en ce qui concerne : la
        qualité des produits entrant dans la composition des repas servis en restauration collective
      </p>
    </div>
    <ul class="fr-col-12 fr-col-lg-5 fr-col-offset-lg-1 fr-grid-row fr-grid-row--gutters ma-cantine--unstyled-list">
      <li class="fr-col-12 fr-col-sm-6">
        <DsfrTile
          titleTag="p"
          title="Accéder à data.gouv.fr"
          to="https://www.data.gouv.fr/fr/organizations/ministere-de-l-agriculture-de-l-agroalimentaire-et-de-la-foret/"
          :imgSrc="pictoDataVisualization"
          small
        />
      </li>
      <li class="fr-col-12 fr-col-sm-6">
        <DsfrTile
          titleTag="p"
          class="observatory-hero__force-title-download-vertical"
          title="Télécharger le rapport annuel 2024"
          :to="documentRapport"
          :imgSrc="pictoDocuments"
          :download="true"
          small
        />
      </li>
    </ul>
  </section>
</template>

<style lang="scss">
.observatory-hero__force-title-download-vertical {
  align-items: center !important;
  flex-direction: column !important;
  justify-content: center !important;
  text-align: center !important;

  .fr-tile__content {
    align-items: center !important;
  }

  .fr-tile__header {
    margin-right: 0 !important;
    margin-bottom: 1rem !important;
  }

  .fr-tile__pictogram {
    height: 3.5rem !important;
  }
}
</style>
