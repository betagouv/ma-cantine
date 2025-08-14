<script setup>
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
import ObservatoryGraphProductionType from "@/components/ObservatoryGraphProductionType.vue"
import ObservatoryGraphEconomicModel from "@/components/ObservatoryGraphEconomicModel.vue"
import ObservatoryGraphManagementType from "@/components/ObservatoryGraphManagementType.vue"
import ObservatoryGraphSectors from "@/components/ObservatoryGraphSectors.vue"

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
    <ol class="fr-grid-row fr-grid-row--gutters ma-cantine--ordered-list ma-cantine--unstyled-list">
      <li class="fr-col-12 fr-col-md-6 fr-mb-4w">
        <ObservatoryGraphEconomicModel :economicModels="stats.economicModels" :canteensCount="stats.canteenCount" />
      </li>
      <li class="fr-col-12 fr-col-md-6 fr-mb-4w">
        <ObservatoryGraphManagementType :managementTypes="stats.managementTypes" :canteensCount="stats.canteenCount" />
      </li>
      <li class="fr-col-12 fr-mb-4w">
        <ObservatoryGraphProductionType :productionTypes="stats.productionTypes" :canteensCount="stats.canteenCount" />
      </li>
      <li class="fr-col-12">
        <ObservatoryGraphSectors :sectorCategories="stats.sectorCategories" :canteensCount="stats.canteenCount" />
      </li>
    </ol>
  </div>
</template>
