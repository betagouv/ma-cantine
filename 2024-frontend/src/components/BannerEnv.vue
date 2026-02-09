<script setup>
import { computed } from 'vue'
const displayBanner = computed(() => window.ENVIRONMENT !== "prod")
</script>
<template>
  <DsfrNotice v-if="displayBanner" type="warning" title="Environnement de démonstration : toutes les actions sont sans conséquence." />
</template>
