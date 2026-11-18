<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import { useStoreCanteen } from '@/stores/canteen'
import urlService from '@/services/urls.js'
import documentation from '@/data/documentation.json'
import AppLinkRouter from '@/components/AppLinkRouter.vue'
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
const circuitCourtFields = [
  "valeurViandesVolaillesCircuitCourt",
  "valeurProduitsDeLaMerCircuitCourt",
  "valeurCharcuterieCircuitCourt",
  "valeurFruitsEtLegumesCircuitCourt",
  "valeurProduitsLaitiersCircuitCourt",
  "valeurBoulangerieCircuitCourt",
  "valeurAutresCircuitCourt",
  "valeurBoissonsCircuitCourt",
]
const localFields = [
  "valeurViandesVolaillesLocal",
  "valeurProduitsDeLaMerLocal",
  "valeurCharcuterieLocal",
  "valeurFruitsEtLegumesLocal",
  "valeurProduitsLaitiersLocal",
  "valeurBoulangerieLocal",
  "valeurAutresLocal",
  "valeurBoissonsLocal",
]

/* Groupe */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const isGroupe = computed(() => canteenInformations.value.isGroupe)
const canteenPage = computed(() => ({
  name: 'CanteenPage',
  params: { canteenUrlComponent: urlService.getCanteenUrl(canteenInformations.value) },
}))

/* Définition du local : la distance n'est attendue que pour le périmètre "KM" */
const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic, isComplete } = storeToRefs(storeTeledeclaration)
const isDefinitionLocalKm = computed(() => diagnostic.value.definitionLocal === "KM")
const updateDefinitionLocal = (value) => {
  if (value !== "KM") storeTeledeclaration.setValue("definitionLocalKm", null)
}
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12">
      <h2>« Local » et circuit court</h2>
      <p class="fr-mb-0">
        Cette dernière étape du volet « Approvisionnements » de la télédéclaration est facultative.
        <template v-if="!isGroupe">
          Elle vous permet de valoriser vos efforts d’approvisionnements sur
          <AppLinkRouter :to="canteenPage" title="la page publique de votre cantine" :is-blank="true" />.
        </template>
        En fonction de votre méthode de suivi, vous pouvez renseigner l’origine : pour une ou plusieurs familles, pour chacune des familles, ou pour le total de vos achats.
      </p>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Achats en circuit court" :documentation="documentation.circuitCourt" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12">
        <TunnelTeledeclarationField name="valeurCircuitCourt" />
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in circuitCourtFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Achats en produits « locaux »" :documentation="documentation.produitsLocaux" />
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12">
        <TunnelTeledeclarationField name="valeurLocal" />
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="definitionLocal" @change="updateDefinitionLocal" />
      </div>
      <div v-if="isDefinitionLocalKm" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField name="definitionLocalKm" />
      </div>
    </div>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in localFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
  <div v-if="!isComplete" class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="Total des achats par famille de produits" />
    <p>
      Pour chaque famille de produits renseignée dans les achats en circuit court ou en « local », vous devez déclarer
      le total des achats de cette famille.
    </p>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div v-for="field in totalAchatsFields" :key="field" class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="field" />
      </div>
    </div>
  </div>
</template>
