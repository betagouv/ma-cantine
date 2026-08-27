<script setup>
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

const bioSiqoFields = ["valeurBio", "valeurBioDontCommerceEquitable", "valeurSiqo"]
const autresEgalimFields = ["valeurEgalimAutres", "valeurEgalimAutresDontCommerceEquitable", "valeurExternalitesPerformance"]
const viandeFamilleFields = ["valeurViandesVolailles", "valeurViandesVolaillesEgalim"]
const poissonFamilleFields = ["valeurProduitsDeLaMer", "valeurProduitsDeLaMerEgalim"]
const autresFamillesFields = ["valeurCharcuterie", "valeurFruitsEtLegumes", "valeurProduitsLaitiers", "valeurBoulangerie", "valeurAutres", "valeurBoissons"]
</script>
<template>
  <div class="fr-mb-4w">
    <h2 class="fr-h6">2. Valeurs totales des achats Bio et SIQO (Label Rouge, AOC / AOP, IGP, STG)</h2>
    <p>Produit ayant plusieurs labels (hors Commerce équitable) : la valeur d’achat doit être comptée uniquement dans une seule des catégories. Par exemple, un produit Bio et Label rouge doit être comptabilisé uniquement dans la catégorie «&nbsp;Bio&nbsp;» ou la catégorie «&nbsp;SIQO&nbsp;».</p>
    <TunnelTeledeclarationField v-for="field in bioSiqoFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h6">3. Valeurs totales des autres achats EGalim ou critères d’achats</h2>
    <TunnelTeledeclarationField v-for="field in autresEgalimFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h6">4. Zoom sur la famille «&nbsp;viandes et volailles&nbsp;»</h2>
    <TunnelTeledeclarationField v-for="field in viandeFamilleFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h6">5. Zoom sur la famille «&nbsp;poissons, produits de la mer et de l’aquaculture&nbsp;»</h2>
    <TunnelTeledeclarationField v-for="field in poissonFamilleFields" :key="field" :name="field" />
  </div>
  <div class="fr-mb-4w">
    <h2 class="fr-h6">6. Zoom sur les autres familles</h2>
    <TunnelTeledeclarationField v-for="field in autresFamillesFields" :key="field" :name="field" />
  </div>
</template>
