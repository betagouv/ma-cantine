<script setup>
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import urlService from "@/services/urls.js"
import AppRessources from "@/components/AppRessources.vue"

/* Router */
const route = useRoute()

/* Canteen */
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-6 fr-mb-4w fr-mb-md-0">
      <h1>{{ route.meta.title }} pour la cantine «&nbsp;{{ canteenName }}&nbsp;»</h1>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <AppRessources>
      <li>
        <a :href="documentation.ajouterAchat" target="_blank">
          Tutoriel pour ajouter un achat manuellement
        </a>
      </li>
      <li>
        <a :href="documentation.critèresQualiteDurabiliteProduits" target="_blank">
          Comprendre les critères de qualité et durabilité des produits
        </a>
      </li>
    </AppRessources>
  </section>
</template>
