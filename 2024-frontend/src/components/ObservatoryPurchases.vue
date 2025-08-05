<script setup>
import keyMeasures from "@/data/key-measures.json"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
import ObservatoryGraphSustainable from "@/components/ObservatoryGraphSustainable.vue"
import ObservatoryGraphFishMeat from "@/components/ObservatoryGraphFishMeat.vue"

defineProps(["stats"])
const approBadge = "/static/images/badges/appro.svg"
const keyMeasureId = keyMeasures[0].id
</script>

<template>
  <div class="observatory-purcharses fr-card fr-p-4w">
    <ObservatoryBadgeTitle class="fr-mb-3w" :image="approBadge" color="#f44336" title="Produits durables et de qualité">
      Distribuer 50% de produits de qualité dont 20% de produits bio et distribuer au moins 60 % de produits durables et
      de qualité dans la famille de denrées “viandes et poissons“.
      <AppLinkRouter :to="{ name: 'KeyMeasurePage', params: { id: keyMeasureId } }" title="En savoir plus sur la loi" />
    </ObservatoryBadgeTitle>
    <ol class="observatory-purcharses__list-graphic ma-cantine--unstyled-list">
      <li class="observatory-purcharses__graphic">
        <ObservatoryGraphSustainable :bioPercent="stats.bioPercent" :egalimPercent="stats.egalimPercent" />
      </li>
      <li class="observatory-purcharses__graphic">
        <ObservatoryGraphFishMeat :meatPercent="stats.meatEgalimPercent" :fishPercent="stats.fishEgalimPercent" />
      </li>
    </ol>
  </div>
</template>

<style lang="scss">
.observatory-purcharses {
  &__list-graphic {
    counter-reset: number;
  }

  &__graphic {
    counter-increment: number;

    &::marker {
      content: initial;
    }

    h3::before {
      content: counter(number) ".";
      margin-right: 0.5rem;
    }
  }
}
</style>
