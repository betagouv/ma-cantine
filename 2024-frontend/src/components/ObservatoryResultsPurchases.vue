<script setup>
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import keyMeasures from "@/data/key-measures.json"

const approBadge = "/static/images/badges/appro.svg"
const keyMeasureId = keyMeasures[0].id
</script>
<template>
  <div class="observatory-results-purchases fr-card fr-p-4w">
    <div class="fr-mb-3w">
      <div class="fr-grid-row fr-grid-row--middle">
        <img :src="approBadge" class="observatory-results-purchases__image" alt="" />
        <h2 class="observatory-results-purchases__title fr-ml-3w fr-h5 fr-mb-0">Produits durables et de qualité</h2>
      </div>
      <p class="fr-pl-9w fr-col-8">
        Distribuer 50% de produits de qualité dont 20% de produits bio et distribuer au moins 60 % de produits durables
        et de qualité dans la famille de denrées “viandes et poissons“.
        <AppLinkRouter
          :to="{ name: 'KeyMeasurePage', params: { id: keyMeasureId } }"
          title="En savoir plus sur la loi"
        />
      </p>
    </div>
  </div>
</template>
<style lang="scss">
.observatory-results-purchases {
  &__image {
    width: 3rem;
    height: 3rem;
  }

  &__title {
    color: #f44336 !important;
  }
}
</style>
