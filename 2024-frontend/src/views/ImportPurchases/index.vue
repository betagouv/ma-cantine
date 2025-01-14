<script setup>
import ImportExplanation from "@/components/ImportExplanation.vue"
const ressources = [
  {
    download: true,
    href: "/static/documents/achats_fichier_exemple_ma_cantine.csv",
    name: "Télécharger notre fichier d’exemple CSV",
    size: "189 octets",
  },
  {
    external: true,
    name: "Comment importer un fichier CSV dans Excel ?",
  },
  {
    external: true,
    href:
      "https://support.microsoft.com/fr-fr/office/enregistrer-un-classeur-au-format-texte-txt-ou-csv-3e9a9d6c-70da-4255-aa28-fcacf1f081e6",
    name: "Comment enregistrer mon fichier Excel en CSV ?",
  },
]
</script>

<template>
  <h1>Créer des achats</h1>
  <p class="fr-col-7">
    Texte d'introduction à venir. Nulla vitae elit libero, a pharetra augue. Aenean lacinia bibendum nulla sed
    consectetur. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit
    amet risus. Nullam quis risus eget urna mollis ornare vel eu leo.
  </p>
  <ImportExplanation :ressources="ressources" />
</template>
