<template>
  <DsfrCallout noIcon>
    <h2 class="fr-text font-weight-bold mb-2 mt-2">
      CAMPAGNE DE TELEDECLARATION 2025 : Du 7 janvier au 31 mars
    </h2>
    <p class="mb-0">
      Dans votre espace cantine, remplissez votre bilan sur les données d'achat 2024 et télédéclarez vos données.
      <br />
      Pour rappel, selon l’arrêté ministériel du 14 septembre 2022, il est obligatoire de télédéclarer ses achats.
    </p>
    <v-row class="mt-4 mb-0 mx-0 align-center">
      <v-btn :to="{ name: 'PendingActions' }" color="primary" class="mb-5 mb-md-2 mr-4">
        Télédéclarer mes cantines
      </v-btn>
      <p class="fr-text-sm mb-5 mb-md-2 mr-4">
        <a
          href="https://894795896-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MSCF7Mdc8yfeIjMxMZr%2Fuploads%2F5ykK6Oj3jbALj2Vfzo48%2FGuide_Campagne_teledeclaration_2024_110124.pdf?alt=media"
          target="_blank"
          rel="noopener external"
          title="Le guide de télédéclaration - ouvre une nouvelle fenêtre"
          class="grey--text text--darken-4"
        >
          Le guide de télédéclaration
          <v-icon small class="ml-2 grey--text text--darken-4">mdi-open-in-new</v-icon>
        </a>
      </p>
      <p class="fr-text-sm mb-5 mb-md-2 mr-4">
        <a
          href="/static/documents/Antisèche_données_d'achat_ma_cantine.pdf"
          download
          title="Antisèche : Préparer la saisie de mes données d'achat"
          class="grey--text text--darken-4"
        >
          Antisèche : Préparer la saisie de mes données d'achat
          <v-icon class="ml-2 grey--text text--darken-4 icon-small" width="1rem">$download-line</v-icon>
        </a>
      </p>
    </v-row>
  </DsfrCallout>
</template>

<script>
import DsfrCallout from "@/components/DsfrCallout"

export default {
  name: "TeledeclarationBanner",
  components: {
    DsfrCallout,
  },
}
</script>

<style scoped>
.v-sheet--shaped {
  border-radius: 26px 4px !important;
}

.icon-small {
  width: 1rem;
}
</style>
