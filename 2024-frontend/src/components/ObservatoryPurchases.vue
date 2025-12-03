<script setup>
import stringsService from "@/services/strings"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
import ObservatoryGraphSustainable from "@/components/ObservatoryGraphSustainable.vue"
import ObservatoryGraphMeatFishEgalim from "@/components/ObservatoryGraphMeatFishEgalim.vue"
import ObservatoryGraphMeatFrance from "@/components/ObservatoryGraphMeatFrance.vue"
import ObservatoryGraphEgalim from "@/components/ObservatoryGraphEgalim.vue"

defineProps(["stats"])
const approBadge = "/static/images/badges/appro.svg"
</script>

<template>
  <div class="observatory-purchases">
    <ObservatoryBadgeTitle class="fr-mb-8w" :image="approBadge" color="#f44336" title="Produits durables et de qualité">
      Distribuer {{ stringsService.prettyPercent(50) }} de produits de qualité dont
      {{ stringsService.prettyPercent(20) }} de produits bio et distribuer au moins
      {{ stringsService.prettyPercent(60) }} de produits durables et de qualité dans la famille de denrées "viandes et
      poissons".
      <AppLinkRouter
        :to="{ name: 'ComprendreMesObligations', params: { id: keyMeasureId } }"
        title="En savoir plus sur la loi"
      />
    </ObservatoryBadgeTitle>
    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li class="fr-mb-8w">
        <ObservatoryGraphEgalim :approPercent="stats.approPercent" />
      </li>
      <li class="fr-mb-8w">
        <ObservatoryGraphSustainable
          :bioPercent="stats.bioPercent"
          :egalimPercent="stats.egalimPercent"
          :bioObjective="stats.notes.bioPercentObjective"
          :egalimObjective="stats.notes.egalimPercentObjective"
        />
      </li>
      <li class="fr-mb-8w">
        <ObservatoryGraphMeatFishEgalim
          :viandesVolaillesProduitsDeLaMerEgalimPercent="stats.viandesVolaillesProduitsDeLaMerEgalimPercent"
        />
      </li>
      <li>
        <ObservatoryGraphMeatFrance :viandesVolaillesFrancePercent="stats.viandesVolaillesFrancePercent" />
      </li>
    </ol>
  </div>
</template>
