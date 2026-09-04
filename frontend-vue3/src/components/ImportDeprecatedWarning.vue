<script setup>
import AppLinkRouter from "@/components/AppLinkRouter.vue"
defineProps(["redirectTo"])
</script>

<template>
  <DsfrCallout icon="fr-icon-warning-line" title="Mise à jour des imports achats">
    <p>
      En 2026, un nouveau format d'import des achats a été mis en place afin de mieux distinguer les catégories EGalim, l'origine, le local et le circuit court dans vos tableurs. Vous pouvez continuer à utiliser cet ancien format d'import jusqu'à la fin de la campagne de télédéclaration 2027, passé ce délai l'import d'achats devra respecter le nouveau format.
      <AppLinkRouter :to="redirectTo" title="Découvrir le nouveau format d'import" />
    </p>
  </DsfrCallout>
</template>
