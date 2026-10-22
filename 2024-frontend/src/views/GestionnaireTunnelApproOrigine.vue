<script setup>
import AppHelpCard from '@/components/AppHelpCard.vue'
import TunnelTeledeclarationUPSABanner from '@/components/TunnelTeledeclarationUPSABanner.vue'
import documentation from '@/data/documentation.json'
import TunnelTeledeclarationField from '@/components/TunnelTeledeclarationField.vue'
import TunnelTeledeclarationGroupTitle from '@/components/TunnelTeledeclarationGroupTitle.vue'

const totalAchatsFields = [
  "valeurViandesVolailles",
  "valeurProduitsDeLaMer",
  "valeurCharcuterie",
  "valeurFruitsEtLegumes",
  "valeurProduitsLaitiers",
  "valeurBoulangerie",
  "valeurAutres",
  "valeurBoissons",
]
const franceFields = [
  "valeurViandesVolaillesFrance",
  "valeurProduitsDeLaMerFrance",
  "valeurCharcuterieFrance",
  "valeurFruitsEtLegumesFrance",
  "valeurProduitsLaitiersFrance",
  "valeurBoulangerieFrance",
  "valeurAutresFrance",
  "valeurBoissonsFrance",
]
const europeFields = [
  "valeurViandesVolaillesEurope",
  "valeurProduitsDeLaMerEurope",
  "valeurCharcuterieEurope",
  "valeurFruitsEtLegumesEurope",
  "valeurProduitsLaitiersEurope",
  "valeurBoulangerieEurope",
  "valeurAutresEurope",
  "valeurBoissonsEurope",
]
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
        <p>
          La télédéclaration sur l'origine des produits peut être réalisée sur certaines familles de produits et/ou sur
          le total de vos approvisionnements.
        </p>
        <p>
          En accord avec la loi UPSA, le suivi de l'origine des produits (Europe et France) sera rendu obligatoire dès
          la campagne de télédéclaration 2028.
        </p>
        <a :href="documentation.origineFrance" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="1. Achats origine France" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12">
        <TunnelTeledeclarationField name="valeurFrance" />
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in franceFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="2. Achats origine Europe (hors France)" />
    <p>
      Achats issus de l'Union Européenne (UE), de l'Espace économique européen (EEE) ou des pays et territoires
      d'outre-mer (PTOM)
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12">
        <TunnelTeledeclarationField name="valeurEurope" />
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in europeFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="3. Total des achats par famille de produits" />
    <p>
      Pour chaque famille de produits renseignée dans les achats origine France ou origine Europe (hors France), vous
      devez déclarer le total des achats de cette famille.
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in totalAchatsFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
</template>
