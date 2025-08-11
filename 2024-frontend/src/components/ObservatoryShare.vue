<script setup>
import { ref } from "vue"

const icon = ref("fr-icon-clipboard-line")
const label = ref("Copier l’url de la recherche")

const copyUrl = () => {
  label.value = "Copié dans le presse-papier"
  icon.value = "fr-icon-check-line"
  navigator.clipboard.writeText(window.location.href)
}
</script>
<template>
  <div class="fr-mt-4w fr-grid-row fr-grid-row--right">
    <DsfrButton :label="label" secondary :icon="icon" @click="copyUrl" />
  </div>
</template>
