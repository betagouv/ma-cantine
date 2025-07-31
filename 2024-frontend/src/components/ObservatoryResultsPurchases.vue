<script setup>
const approBadge = "/static/images/badges/appro.svg"
</script>
<template>
  <div class="observatory-results-purchases fr-card fr-p-4w">
    <div class="fr-grid-row fr-grid-row--middle">
      <img :src="approBadge" class="observatory-results-purchases__image" alt="" />
      <h2 class="observatory-results-purchases__title fr-ml-3w fr-h5 fr-mb-0">Produits durables et de qualité</h2>
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
