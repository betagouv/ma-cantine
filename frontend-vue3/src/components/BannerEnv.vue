<script setup>
import { computed } from 'vue'
const displayBanner = computed(() => window.ENVIRONMENT !== "prod")
</script>
<template>
  <DsfrNotice v-if="displayBanner" type="warning" title="Environnement de démonstration : toutes les actions sont sans conséquence." desc="Le comportement est figé sur la période de télédéclaration (possibilité de créer un bilan de l'année n-1 et de le télédéclarer/corriger jusqu'à la fin de l'année n)" />
</template>
