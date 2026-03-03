<script setup>
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"

const route = useRoute()
const pictoDataVisualization = "/static/images/picto-dsfr/data-visualization.svg"
const pictoDocuments = "/static/images/picto-dsfr/documents.svg"
</script>

<template>
  <section class="fr-grid-row fr-grid-row--gutters fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-lg-6">
      <h1>{{ route.meta.title }}</h1>
      <p>
        La loi EGalim, complétée par la loi Climat et Résilience, a défini des obligations de qualité et durabilité des produits entrant dans la composition des repas et de lutte contre le gaspillage alimentaire et d’information des convives. Des obligations en matière de diversification des sources de protéines et de mise en place de menus végétariens sont également en vigueur (selon secteurs et/ou nombre de repas servis).
      </p>
      <p>
        Cette  version de l’Observatoire met à disposition uniquement les données relatives à la qualité et la durabilité des produits. Pour comprendre comment sont calculés les indicateurs, leurs spécificités, et les évolutions à venir :
        <a
          href="https://incubateur-masa.notion.site/A-propos-de-l-observatoire-EGalim-en-restauration-collective-262de24614be800d8924eb83901def36"
          target="_blank"
        >
          consulter notre article explicatif
        </a>
      </p>
      <p class="fr-mb-0">
        Les chiffres de l’année n-1 sont rendus publics en année n, dès publication du bilan statistique annuel (rapport du gouvernement au parlement).
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
          :to="documentation.rapportsBilansStatistiquesEgalim"
          :imgSrc="pictoDocuments"
          small
        />
      </li>
    </ul>
  </section>
</template>
