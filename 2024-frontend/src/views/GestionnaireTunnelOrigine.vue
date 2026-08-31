<script setup>
import AppHelpCard from '@/components/AppHelpCard.vue'
import documentation from '@/data/documentation.json'

</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Origine France et UE</h2>
      <p class="fr-mb-0">Ces données ne sont pas obligatoires pour valider votre déclaration. Ici, vous pouvez affecter le produit dans plusieurs caractéristiques. Par exemple, un produit à la fois biologique et local pourra être comptabilisé dans les deux champs “bio” et “local”.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="À propos de l’origine France">
        <a :href="documentation.origineFrance" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
</template>
