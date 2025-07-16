<script setup>
import { useTemplateRef } from "vue"
import { useRoute } from "vue-router"
import AppFilters from "@/components/AppFilters.vue"
import ObservatoryResultsFilters from "@/components/ObservatoryResultsFilters.vue"

const route = useRoute()
const pictoDataVisualization = "/static/images/picto-dsfr/data-visualization.svg"
const pictoDocuments = "/static/images/picto-dsfr/documents.svg"
const documentRapport = "/static/documents/Rapport_Bilan_Statistique_EGALIM_2024.pdf"
const filtersRef = useTemplateRef("filters-ref")

const scrollToFilters = () => {
  filtersRef.value.scrollIntoView({ behavior: "smooth" })
}
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
          class="observatoire__force-title-download-vertical"
          title="Télécharger le rapport annuel 2024"
          :to="documentRapport"
          :imgSrc="pictoDocuments"
          :download="true"
          small
        />
      </li>
    </ul>
  </section>
  <section class="fr-pt-5w" ref="filters-ref">
    <h2 class="fr-h5">Retrouver les chiffres clés sur votre territoire</h2>
    <AppFilters />
  </section>
  <section class="observatoire__results ma-cantine--sticky__container fr-mt-4w fr-pb-4w">
    <ObservatoryResultsFilters @scrollToFilters="scrollToFilters()" class="ma-cantine--sticky__top" />
    <br />
    <br />
    <br />
    <br />
    <br />
    <div style="height: 100vh">
      Contenu
    </div>
  </section>
</template>

<style lang="scss">
.observatoire {
  &__force-title-download-vertical {
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

  &__results {
    &::before {
      z-index: -1;
      content: "";
      background-color: var(--background-alt-blue-france);
      position: absolute;
      top: 0;
      left: calc((100vw - 100%) / 2 * -1);
      width: 100vw;
      height: 100%;
    }
  }
}
</style>
