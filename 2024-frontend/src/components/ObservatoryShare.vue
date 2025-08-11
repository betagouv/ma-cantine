<script setup>
import { ref } from "vue"

const icon = ref()
const label = ref()

const copyUrl = () => {
  navigator.clipboard.writeText(window.location.href)
  updateButton("copied")
  setTimeout(updateButton, 5000)
}

/* Change button content */
const updateButton = (state) => {
  const isCopied = state === "copied"
  label.value = isCopied ? "Copié dans le presse-papier" : "Copier l’url de la recherche"
  icon.value = isCopied ? "fr-icon-check-line" : "fr-icon-clipboard-line"
}
updateButton()
</script>
<template>
  <div class="fr-mt-4w fr-grid-row fr-grid-row--right">
    <DsfrButton :label="label" secondary :icon="icon" @click="copyUrl" />
  </div>
</template>
