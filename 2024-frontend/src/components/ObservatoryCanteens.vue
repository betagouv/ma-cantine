<script setup>
import ObservatoryBadgeTitle from "@/components/ObservatoryBadgeTitle.vue"
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
      Tous les restaurants collectifs on l'obligation de s'inscrire sur ma cantine et de télédéclarer, chaque année,
      leur bilan annuel de l'année précédente.
    </ObservatoryBadgeTitle>
  </div>
</template>
