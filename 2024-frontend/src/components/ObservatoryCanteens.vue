<script setup>
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
import ObservatoryGraphProductionType from "@/components/ObservatoryGraphProductionType.vue"
import ObservatoryGraphEconomicModel from "@/components/ObservatoryGraphEconomicModel.vue"

defineProps(["stats"])
const canteenBadge = "/static/images/badges/canteen.svg"
</script>

<template>
  <div>
    <ObservatoryBadgeTitle
      class="fr-mb-8w"
      :image="canteenBadge"
      color="#000090"
      title="Les restaurants collectifs du territoire"
    >
      Tous les restaurants collectifs ont l'obligation de s'inscrire sur ma cantine et de télédéclarer, chaque année,
      leur bilan annuel de l'année précédente.
    </ObservatoryBadgeTitle>
    <ol class="ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li>
        <ObservatoryGraphProductionType :productionTypes="stats.productionTypes" :canteensCount="stats.canteenCount" />
      </li>
      <li>
        <ObservatoryGraphEconomicModel :economicModels="stats.economicModels" :canteensCount="stats.canteenCount" />
      </li>
    </ol>
  </div>
</template>
