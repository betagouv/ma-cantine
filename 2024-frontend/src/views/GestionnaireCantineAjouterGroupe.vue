<script setup>
import { useRoute } from "vue-router"
import AppRessources from "@/components/AppRessources.vue"

/* Router and Store */
const route = useRoute()
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-6 fr-mb-4w fr-mb-md-0">
      <h1>{{ route.meta.title }}</h1>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <AppRessources>
      <li>
        <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">
          Annuaire des entreprises pour trouver le SIREN
        </a>
      </li>
    </AppRessources>
  </section>
</template>
