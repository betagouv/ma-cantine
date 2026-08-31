<script setup>
import AppHelpCard from '@/components/AppHelpCard.vue'
import documentation from '@/data/documentation.json'
import TunnelTeledeclarationField from '@/components/TunnelTeledeclarationField.vue'

const fieldsFR = ["valeurFrance", "valeurViandesVolaillesFrance", "valeurProduitsDeLaMerFrance", "valeurFruitsEtLegumesFrance", "valeurCharcuterieFrance", "valeurProduitsLaitiersFrance", "valeurBoulangerieFrance", "valeurBoissonsFrance", "valeurAutresFrance"]
const fieldsEU = ["valeurEurope", "valeurViandesVolaillesEurope", "valeurProduitsDeLaMerEurope", "valeurFruitsEtLegumesEurope", "valeurCharcuterieEurope", "valeurProduitsLaitiersEurope", "valeurBoulangerieEurope", "valeurBoissonsEurope", "valeurAutresEurope"]
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-0">Ces données ne sont pas obligatoires pour valider votre déclaration. Ici, vous pouvez affecter le produit dans plusieurs caractéristiques. Par exemple, un produit à la fois biologique et français pourra être comptabilisé dans les deux champs “bio” et “france”.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="À propos de l’origine France">
        <a :href="documentation.origineFrance" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <h3 class="fr-h5">1. Valeurs totales des achats origine France</h3>
  <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
    <TunnelTeledeclarationField v-for="field in fieldsFR" :key="field" :name="field" size="inline" />
  </div>
  <h3 class="fr-h5">2. Valeurs totales des achats origine UE (hors France)</h3>
  <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
    <TunnelTeledeclarationField v-for="field in fieldsEU" :key="field" :name="field" size="inline" />
  </div>
</template>
