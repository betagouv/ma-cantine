<script setup>
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"

import AppPictoAdd from "@/components/AppPictoAdd.vue"

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
    Notre outil d’import de masse vous permet d’ajouter les achats de toutes vos cantines d’un coup.
    <strong>Si vous avez moins de 10 achats,</strong>
    il est plus rapide de les saisir directement
    <router-link :to="{ name: 'PurchasesHome' }">sur la plateforme</router-link>
    .
  </p>
  <ImportExplanation :ressources="ressources" />
  <ImportSchemaTable
    url="https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main/data/schemas/imports/achats.json"
  />
  <section
    class="fr-px-6w fr-px-xl-9w fr-py-6w fr-background-alt--blue-france fr-mt-4w fr-grid-row fr-grid-row--middle"
  >
    <AppPictoAdd class="fr-hidden fr-unhidden-xl fr-col-3 fr-pr-6w" />
    <div class="import-file-upload fr-col-12 fr-col-xl-9 fr-py-3w fr-px-4w fr-card">
      <DsfrFileUpload
        label="Avant d’importer votre fichier en CSV, assurez-vous que vos données respectent le format ci-dessus"
        accept="csv"
        hint="Extension du fichier autorisé : CSV"
      />
    </div>
  </section>
</template>

<style lang="scss">
.import-file-upload {
  .fr-label {
    font-weight: 700;
    max-width: 75%;

    span {
      font-weight: initial;
    }
  }
}
</style>
