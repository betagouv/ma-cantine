<script setup>
import AppLinkRouter from "@/components/AppLinkRouter.vue"
</script>
<template>
  <DsfrAlert
    type="info"
    title="Nouveauté EGalim : la loi UPSA élargit les catégories de produits éligibles depuis le 18 août 2026."
    class="fr-mb-4w"
  >
    <p>
      En phase transitoire, comptabilisez ces produits dans les catégories existantes. De nouvelles catégories seront
      créées pour la télédéclaration 2028. En savoir plus :
      <AppLinkRouter :to="{ name: 'ComprendreMesObligations' }" title="Comprendre mes obligations" />
    </p>
  </DsfrAlert>
</template>
