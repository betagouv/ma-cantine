<script setup>
import { useRoute } from "vue-router"
import AppFilters from "@/components/AppFilters.vue"

const route = useRoute()
const pictoDataVisualization = "/static/images/picto-dsfr/data-visualization.svg"
const pictoDocuments = "/static/images/picto-dsfr/documents.svg"
</script>

<template>
  <section class="fr-grid-row fr-grid-row--gutters fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-lg-6">
      <h1>{{ route.meta.title }}</h1>
      <p>
        Pour la restauration collective, la loi EGalim, complétée par la loi Climat et Résilience, a défini des
        obligations en ce qui concerne : la qualité des produits entrant dans la composition des repas servis en
        restauration collective, la mise en place d’un menu végétarien, la lutte contre le gaspillage alimentaire et la
        réduction des plastiques à usage unique.
      </p>
      <p>
        Afin de visualiser rapidemment ... Maecenas faucibus mollis interdum. Cras mattis consectetur purus sit amet
        fermentum. Vestibulum id ligula porta felis euismod semper. Vestibulum id ligula porta felis euismod semper. Sed
        posuere consectetur est at lobortis. Aenean lacinia bibendum nulla sed consectetur.
      </p>
    </div>
    <ul class="fr-col-12 fr-col-lg-5 fr-col-offset-lg-1 fr-grid-row fr-grid-row--gutters ma-cantine--unstyled-list">
      <li class="fr-col-12 fr-col-sm-6">
        <DsfrTile
          titleTag="p"
          class="statistics-canteens__force-title-download-vertical"
          title="Rapport de la campagne 2024"
          description="Application et des objectifs d’approvisionnements fixés à la restauration collective."
          to="/#"
          :imgSrc="pictoDocuments"
          :download="true"
          small
        />
      </li>
      <li class="fr-col-12 fr-col-sm-6">
        <DsfrTile
          titleTag="p"
          title="Consulter data.gouv.fr"
          description="Données du Ministère de l'Agriculture et de l'Alimentation"
          to="https://www.data.gouv.fr/fr/organizations/ministere-de-l-agriculture-de-l-agroalimentaire-et-de-la-foret/"
          :imgSrc="pictoDataVisualization"
          small
        />
      </li>
    </ul>
  </section>
  <section class="fr-mt-5w">
    <h2 class="fr-h5">Retrouver les chiffres clés sur votre territoire</h2>
    <AppFilters />
  </section>
</template>

<style lang="scss">
.statistics-canteens {
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
}
</style>
