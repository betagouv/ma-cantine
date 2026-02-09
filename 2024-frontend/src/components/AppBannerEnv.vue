<script setup>
import { computed } from 'vue'
const env = window.ENVIRONMENT
const displayBanner = computed(() => window.ENVIRONMENT !== "prod")
const envText = computed(() => {
  if (env === "staging") return "DEV"
  if (env === "demo") return "DÉMO"
  return env
})
</script>
<template>
  <DsfrNotice v-if="displayBanner" type="warning" :title="`Vous êtes sur l'environnement ${envText}`" />
</template>
