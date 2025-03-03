<script setup>
import { useRoute } from "vue-router"
import AppRessources from "@/components/AppRessources.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
const route = useRoute()
</script>

<template>
  <section class="fr-grid-row">
    <div class="fr-col-12 fr-col-md-7">
      <h1>{{ route.meta.title }}</h1>
      <p>
        La mission de la plateforme
        <em>ma cantine</em>
        est de référencer toutes les cantines de France afin d’aider le ministère de l’agriculture à déployer sa
        transition alimentaire.
      </p>
      <p>Remplissez le formulaire ci-dessous pour créer votre établissement.</p>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <AppRessources>
      <li>
        <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">
          Annuaire des entreprises pour trouver le SIRET
        </a>
      </li>
      <li>
        <a href="https://annuaire-education.fr/" target="_blank">
          Annuaire des cantines scolaires pour trouver le SIRET
        </a>
      </li>
      <li>
        <AppLinkRouter
          :to="{ name: 'ImportCanteens' }"
          title="Créer plusieurs établissements via un fichier d’import"
        />
      </li>
    </AppRessources>
  </section>
</template>
