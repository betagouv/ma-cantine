<template>
  <v-dialog v-model="showDialog" max-width="600">
    <v-card>
      <div class="pa-4 d-flex align-center" style="background-color: #F5F5F5">
        <v-spacer></v-spacer>
        <v-btn color="primary" outlined @click="showDialog = false">
          Fermer
        </v-btn>
      </div>
      <div class="pa-6">
        <v-card-title class="mb-6">
          <img src="/static/images/picto-dsfr/success.svg" width="50px" />
          <h1 class="fr-h5 mb-0 ml-2">
            Le fichier a été importé avec succès
          </h1>
        </v-card-title>
        <v-card-text class="text-left">
          <v-row class="mb-4 ml-0 mr-0">
            <p class="font-weight-bold">{{ description }}</p>
            <p>
              Depuis votre tableau de bord, vous devez télédéclarer vos données, lorsque la campagne de télédéclaration
              est ouverte.
            </p>
          </v-row>
          <v-row>
            <v-spacer></v-spacer>
            <router-link :to="{ name: 'GestionnaireTableauDeBord' }">
              <v-btn color="primary" class="px-4">
                Aller sur mon tableau de bord
              </v-btn>
            </router-link>
          </v-row>
        </v-card-text>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "ImporterSuccessDialog",
  props: {
    description: String,
    isOpen: Boolean,
  },
  data() {
    return {
      showDialog: this.isOpen,
    }
  },
}
</script>
