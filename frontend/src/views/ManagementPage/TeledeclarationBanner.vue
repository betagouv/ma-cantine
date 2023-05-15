<template>
  <v-card color="primary lighten-4" elevation="1" shaped class="d-flex align-center">
    <div>
      <v-card-title class="text-body-1 font-weight-bold">
        PROLONGATION : vous avez jusqu'au 30 juin 2023 pour participer à la collecte de données !
      </v-card-title>
      <v-card-text class="pb-0">
        Dans votre espace cantine, remplissez votre diagnostic 2022 et télédéclarez vos données (arrêté ministériel du
        14 septembre 2022). L'objectif : établir un bilan de suivi des mesures EGAlim permettant de mieux piloter cette
        politique publique par l'administration.
      </v-card-text>
      <v-card-actions class="px-4 mt-2">
        <v-btn :to="{ name: 'PendingActions' }" color="primary">Télédéclarer mes cantines</v-btn>
        <v-btn
          text
          href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/infos-generales-sur-contexte-r%C3%A9glementaire/master/procedure-campagne-de-remontee-des-donnees-annuelle"
          target="_blank"
          rel="noopener"
          class="text-decoration-underline"
        >
          Le guide de télédéclaration
          <v-icon small class="ml-2">mdi-open-in-new</v-icon>
        </v-btn>
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
