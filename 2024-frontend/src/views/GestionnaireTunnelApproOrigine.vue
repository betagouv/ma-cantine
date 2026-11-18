<script setup>
import { storeToRefs } from 'pinia'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import AppHelpCard from '@/components/AppHelpCard.vue'
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

const storeTeledeclaration = useStoreTeledeclaration()
const { isComplete } = storeToRefs(storeTeledeclaration)
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Origine France ou Europe (hors France)</h2>
      <p>
        Cette étape du volet « Approvisionnements » de la télédéclaration est facultative et vient en complémentarité de l’étape sur vos données d’achats EGalim.
      </p>
      <p class="fr-mb-0">
        Pour les champs « Origine France », vous devez comptabiliser les produits originaires de France. Pour les champs « Origine Europe (hors France) », vous devez comptabiliser les produits originaires de l'Union Européenne (UE), de l’Espace économique européen (EEE) ou des pays et territoires d'outre-mer (PTOM).
      </p>
      <p>
        En fonction de votre méthode de suivi, vous pouvez renseigner l’origine : pour une ou plusieurs familles, pour chacune des familles, ou pour le total de vos achats.
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur le suivi et la télédéclaration de l'origine des produits">
        <a :href="documentation.origineFrance" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Achats origine France" />
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
    <TunnelTeledeclarationGroupTitle title="Achats origine Europe (hors France)" />
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
  <div v-if="!isComplete" class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Total des achats par famille de produits" />
    <p class="fr-mb-2w">
      Pour chaque famille de produits renseignée dans les achats origine France ou origine Europe (hors France), vous devez déclarer le total des achats de cette famille. Les montants déjà inscrits sont issus de votre déclaration des données EGalim.
    </p>
    <DsfrHighlight class="fr-ml-0 fr-mb-2w">
      <p>
        <span class="fr-text--bold">Exemple :</span><br />
        Vous indiquez 35€ de Charcuteries Origine France, vous devez donc préciser ici le total des achats de Charcuteries effectués dans l’année.
      </p>
    </DsfrHighlight>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in totalAchatsFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
</template>
