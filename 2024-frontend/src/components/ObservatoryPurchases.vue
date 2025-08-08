<script setup>
import keyMeasures from "@/data/key-measures.json"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
import ObservatoryGraphSustainable from "@/components/ObservatoryGraphSustainable.vue"
import ObservatoryGraphFishMeat from "@/components/ObservatoryGraphFishMeat.vue"
import ObservatoryGraphMeatFrance from "@/components/ObservatoryGraphMeatFrance.vue"
import ObservatoryGraphEgalim from "@/components/ObservatoryGraphEgalim.vue"

defineProps(["stats"])
const approBadge = "/static/images/badges/appro.svg"
const keyMeasureId = keyMeasures[0].id
</script>

<template>
  <div class="observatory-purchases">
    <ObservatoryBadgeTitle class="fr-mb-8w" :image="approBadge" color="#f44336" title="Produits durables et de qualité">
      Distribuer 50% de produits de qualité dont 20% de produits bio et distribuer au moins 60% de produits durables et
      de qualité dans la famille de denrées “viandes et poissons“.
      <AppLinkRouter :to="{ name: 'KeyMeasurePage', params: { id: keyMeasureId } }" title="En savoir plus sur la loi" />
    </ObservatoryBadgeTitle>
    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li>
        <ObservatoryGraphEgalim :approPercent="stats.approPercent" />
      </li>
      <li>
        <ObservatoryGraphSustainable
          :bioPercent="stats.bioPercent"
          :egalimPercent="stats.egalimPercent"
          :bioObjective="stats.notes.bioPercentObjective"
          :egalimObjective="stats.notes.egalimPercentObjective"
        />
      </li>
      <li>
        <ObservatoryGraphFishMeat :meatPercent="stats.meatEgalimPercent" :fishPercent="stats.fishEgalimPercent" />
      </li>
      <li>
        <ObservatoryGraphMeatFrance :meatFrancePercent="stats.meatFrancePercent" />
      </li>
    </ol>
  </div>
</template>
