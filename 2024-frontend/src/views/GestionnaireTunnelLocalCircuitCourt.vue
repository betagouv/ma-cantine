<script setup>
import TunnelTeledeclarationField from '@/components/TunnelTeledeclarationField.vue'
import AppHelpCard from '@/components/AppHelpCard.vue'
import documentation from '@/data/documentation.json'

const fieldsCircuitCourt = ["valeurCircuitCourt", "valeurViandesVolaillesCircuitCourt", "valeurProduitsDeLaMerCircuitCourt", "valeurFruitsEtLegumesCircuitCourt", "valeurCharcuterieCircuitCourt", "valeurProduitsLaitiersCircuitCourt", "valeurBoulangerieCircuitCourt", "valeurBoissonsCircuitCourt", "valeurAutresCircuitCourt"]
const fieldsLocal = ["definitionLocal", "definitionLocalKm", "valeurLocal", "valeurViandesVolaillesLocal", "valeurProduitsDeLaMerLocal", "valeurFruitsEtLegumesLocal", "valeurCharcuterieLocal", "valeurProduitsLaitiersLocal", "valeurBoulangerieLocal", "valeurBoissonsLocal", "valeurAutresLocal"]
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <p class="fr-mb-0">Ces données ne sont pas obligatoires pour valider votre déclaration. Ici, vous pouvez affecter le produit dans plusieurs caractéristiques. Par exemple, un produit à la fois biologique et local pourra être comptabilisé dans les deux champs “bio” et “local”.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="À propos des achats «&nbsp;locaux&nbsp;» et circuits courts">
        <a :href="documentation.accueil" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <h3 class="fr-h6">1. Valeurs totales des achats « Locaux »</h3>
  <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
    <TunnelTeledeclarationField v-for="field in fieldsLocal" :key="field" :name="field" size="inline" />
  </div>
  <h3 class="fr-h6">2. Valeurs totales des achats circuits courts ou approvisionnements directs</h3>
  <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
    <TunnelTeledeclarationField v-for="field in fieldsCircuitCourt" :key="field" :name="field" size="inline" />
  </div>
</template>
