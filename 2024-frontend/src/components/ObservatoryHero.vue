<script setup>
import { useRoute } from "vue-router"

const route = useRoute()
const pictoDataVisualization = "/static/images/picto-dsfr/data-visualization.svg"
const pictoDocuments = "/static/images/picto-dsfr/documents.svg"
</script>

<template>
  <section class="fr-grid-row fr-grid-row--gutters fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-lg-6">
      <h1>{{ route.meta.title }}</h1>
      <p>
        La loi EGalim, complétée par la loi Climat et Résilience, a défini des obligations en ce qui concerne : la
        qualité des produits entrant dans la composition des repas servis en restauration collective.
      </p>
      <p class="fr-mb-0">
        Ces chiffres sont rendus publics tous les ans après la publication du rapport parlementaire. Pour comprendre
        comment sont calculés les chiffres et leurs spécificités,
        <a
          href="https://incubateur-masa.notion.site/A-propos-de-l-observatoire-EGalim-en-restauration-collective-262de24614be800d8924eb83901def36"
          target="_blank"
        >
          consulter notre article explicatif
        </a>
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
          title="Accéder aux bilans statistiques EGalim"
          to="https://ma-cantine.crisp.help/fr/article/rapports-bilans-statistiques-egalim-de-la-restauration-collective-18z8ru0/"
          :imgSrc="pictoDocuments"
          small
        />
      </li>
    </ul>
  </section>
</template>
