<template>
  <v-dialog v-model="showDialog" max-width="600">
    <v-card class="pt-4">
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
        <v-row justify="center" class="mb-2 ml-0 mr-0">
          <v-btn color="primary" outlined class="px-4 mr-2" @click="showDialog = false">
            Fermer
          </v-btn>
          <router-link :to="{ name: 'ManagementPage' }">
            <v-btn color="primary" class="px-4">
              Aller sur mon tableau de bord
            </v-btn>
          </router-link>
        </v-row>
      </v-card-text>
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
