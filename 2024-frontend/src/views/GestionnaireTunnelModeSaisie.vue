<script setup>
import AppHelpCard from "@/components/AppHelpCard.vue"
import documentation from "@/data/documentation.json"
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Choisissez votre mode de saisie</h2>
      <p>Deux formats existent pour les modes de saisie des données d’approvisionnements EGalim. Un troisième est disponible si vous utilisez l'Outil de Suivi des Achats <em>ma cantine</em>.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Télédéclaration simplifiée ou détaillée : laquelle choisir ?">
        <a target="_blank" :href="documentation.teledeclarationType">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
</template>
