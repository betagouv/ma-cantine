<script setup>
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import ObservatoryCardTitle from "@/components/ObservatoryCardTitle.vue"
import keyMeasures from "@/data/key-measures.json"

const approBadge = "/static/images/badges/appro.svg"
const keyMeasureId = keyMeasures[0].id
</script>

<template>
  <div class="fr-card fr-p-4w">
    <ObservatoryCardTitle class="fr-mb-3w" :image="approBadge" color="#f44336" title="Produits durables et de qualité">
      Distribuer 50% de produits de qualité dont 20% de produits bio et distribuer au moins 60 % de produits durables et
      de qualité dans la famille de denrées “viandes et poissons“.
      <AppLinkRouter :to="{ name: 'KeyMeasurePage', params: { id: keyMeasureId } }" title="En savoir plus sur la loi" />
    </ObservatoryCardTitle>
  </div>
</template>
