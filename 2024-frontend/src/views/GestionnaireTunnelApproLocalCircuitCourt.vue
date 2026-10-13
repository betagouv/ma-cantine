<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import AppHelpCard from '@/components/AppHelpCard.vue'
import documentation from '@/data/documentation.json'
import TunnelTeledeclarationField from '@/components/TunnelTeledeclarationField.vue'
import TunnelTeledeclarationGroupTitle from '@/components/TunnelTeledeclarationGroupTitle.vue'

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

/* Définition du local : la distance n'est attendue que pour le périmètre "KM" */
const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(storeTeledeclaration)
const isDefinitionLocalKm = computed(() => diagnostic.value.definitionLocal === "KM")
const updateDefinitionLocal = (value) => {
  if (value !== "KM") storeTeledeclaration.setValue("definitionLocalKm", null)
}
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-6">
      <h2>« Local » et circuit court</h2>
      <p class="fr-mb-0">
        Ces données ne sont pas obligatoires pour valider votre déclaration. Ici, vous pouvez affecter le produit dans
        plusieurs caractéristiques. Par exemple, un produit à la fois biologique et local pourra être comptabilisé dans
        les deux champs “bio” et “local”.
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-6">
      <AppHelpCard title="À propos des achats «&nbsp;locaux&nbsp;» et circuits courts">
        <a :href="documentation.accueil" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mb-6w">
    <TunnelTeledeclarationGroupTitle title="1. Achats en circuit court" :documentation="documentation.accueil" />
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
    <TunnelTeledeclarationGroupTitle title="2. Achats en produits « locaux »" :documentation="documentation.produitsLocaux" />
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
</template>
