<script setup>
import documentation from "@/data/documentation.json"
</script>
<template>
  <DsfrAlert type="info" class="tunnel-teledeclaration-upsa-banner fr-mb-4w">
    <div class="fr-mb-1w">
      <DsfrBadge label="Nouveauté loi UPSA" type="new" class="tunnel-teledeclaration-upsa-banner__badge" />
      <p class="tunnel-teledeclaration-upsa-banner__title fr-h6">
        Élargissement des catégories de produits éligibles depuis le 18 août 2026.
      </p>
    </div>
    <p>
      En phase transitoire, comptabilisez ces produits dans les catégories existantes. De nouvelles catégories seront
      créées pour la télédéclaration 2028.
      <a :href="documentation.loiUPSA" target="_blank">En savoir plus</a>
    </p>
  </DsfrAlert>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-upsa-banner {
  &__badge {
    vertical-align: middle;
  }

  &__title {
    display: inline;
    vertical-align: middle;
  }
}
</style>
