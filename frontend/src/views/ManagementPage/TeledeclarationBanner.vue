<template>
  <v-card color="primary lighten-4" elevation="1" shaped class="d-flex align-center">
    <div>
      <v-card-title class="text-body-1 font-weight-bold">
        <p class="mb-0">CAMPAGNE DE TELEDECLARATION 2024 : prolongation exceptionnelle jusqu'au 15 avril !</p>
      </v-card-title>
      <v-card-text class="pb-0">
        <p class="mb-0">
          Dans votre espace cantine, remplissez votre bilan sur les données d'achat 2023 et télédéclarez vos données
          (arrêté ministériel du 14 septembre 2022 - en cours de modification). L'objectif : établir un bilan de suivi
          des mesures EGAlim permettant de mieux piloter cette politique publique par l'administration.
        </p>
      </v-card-text>
      <v-card-actions class="px-4 pb-2 mt-2">
        <p class="mb-0">
          <v-btn :to="{ name: 'PendingActions' }" color="primary" class="mb-2 mr-4">
            Télédéclarer mes cantines
          </v-btn>
          <v-btn
            text
            href="https://894795896-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MSCF7Mdc8yfeIjMxMZr%2Fuploads%2F5ykK6Oj3jbALj2Vfzo48%2FGuide_Campagne_teledeclaration_2024_110124.pdf?alt=media"
            target="_blank"
            rel="noopener"
            class="text-decoration-underline mb-2 ml-n4 mr-4"
          >
            Le guide de télédéclaration
            <v-icon small class="ml-2">mdi-open-in-new</v-icon>
          </v-btn>
          <v-btn
            text
            href="https://1648047458-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MSCF7Mdc8yfeIjMxMZr%2Fuploads%2FlNPOtFoTKyfj5UnjZKJj%2FEGAlim%20Bilan%20statistique%202023%20d%C3%A9finitif.pdf?alt=media"
            target="_blank"
            rel="noopener"
            class="text-decoration-underline mb-2 ml-n4"
          >
            Bilan EGAlim pour la campagne de 2022
            <v-icon small class="ml-2">mdi-open-in-new</v-icon>
          </v-btn>
        </p>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "TeledeclarationBanner",
}
</script>

<style scoped>
.v-sheet--shaped {
  border-radius: 26px 4px !important;
}
</style>
