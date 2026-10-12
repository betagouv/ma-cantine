<script setup>
import AppHelpCard from '@/components/AppHelpCard.vue'
import TunnelTeledeclarationUPSABanner from '@/components/TunnelTeledeclarationUPSABanner.vue'
import documentation from '@/data/documentation.json'
import TunnelTeledeclarationField from '@/components/TunnelTeledeclarationField.vue'

const fieldsFR = ["valeurFrance", "valeurViandesVolaillesFrance", "valeurProduitsDeLaMerFrance", "valeurFruitsEtLegumesFrance", "valeurCharcuterieFrance", "valeurProduitsLaitiersFrance", "valeurBoulangerieFrance", "valeurBoissonsFrance", "valeurAutresFrance"]
const fieldsEU = ["valeurEurope", "valeurViandesVolaillesEurope", "valeurProduitsDeLaMerEurope", "valeurFruitsEtLegumesEurope", "valeurCharcuterieEurope", "valeurProduitsLaitiersEurope", "valeurBoulangerieEurope", "valeurBoissonsEurope", "valeurAutresEurope"]
</script>
<template>
  <TunnelTeledeclarationUPSABanner />
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-6">
      <h2>Origine France ou Europe (hors France)</h2>
      <p>
        Étape permettant de renseigner des achats par famille de produit (ou toute famille de produit confondue) au
        regard des catégories d'origine France ou origine Europe (hors France). Vous pouvez renseigner des achats dans
        une seule famille de produit, dans plusieurs familles de produits, ou uniquement le total (dans le cas où vous
        ne suivez pas l'origine par famille).
      </p>
      <p class="fr-mb-0">
        Cette étape est distincte de l'étape de télédéclaration EGalim. Par exemple, l'achat d'un produit bio et
        français doit être renseigné dans la catégorie bio (étape télédéclaration EGalim) ainsi que dans la catégorie
        origine France (étape actuelle).
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-6">
      <AppHelpCard title="En savoir plus sur le suivi et la télédéclaration de l'origine des produits">
        <a :href="documentation.origineFrance" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <h3 class="fr-h5">1. Valeurs totales des achats origine France</h3>
  <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
    <TunnelTeledeclarationField v-for="field in fieldsFR" :key="field" :name="field" />
  </div>
  <h3 class="fr-h5">2. Valeurs totales des achats origine UE (hors France)</h3>
  <div class="fr-mb-4w fr-grid-row fr-grid-row--gutters">
    <TunnelTeledeclarationField v-for="field in fieldsEU" :key="field" :name="field" />
  </div>
</template>
