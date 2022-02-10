<template>
  <div>
    <v-card elevation="0" class="text-center text-md-right">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="150px" contain src="/static/images/SittingChef.png"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="9" md="6">
          <v-card-title class="pl-0 pl-md-10">
            <h1 class="font-weight-black text-h4">Mieux manger de la crêche à l’EHPAD</h1>
          </v-card-title>
          <v-card-text>
            ma-cantine accompagne la transition alimentaire de la restauration collective en outillant les gestionnaires
            afin de fomenter les bonnes pratiques tant en matière de santé que de respect de l’environnement et en
            informant les convives sur le contenu de leur assiette !
          </v-card-text>
        </v-col>
        <v-col cols="12" sm="3" md="3" class="d-flex flex-column" v-if="$vuetify.breakpoint.mdAndUp">
          <v-spacer></v-spacer>
          <v-img max-height="200px" contain src="/static/images/SittingChef.png"></v-img>
          <v-spacer></v-spacer>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>
    <v-row :class="{ 'flex-column': $vuetify.breakpoint.xsAndDown }" justify="center">
      <v-btn
        x-large
        outlined
        color="primary"
        :class="{ 'mr-8': $vuetify.breakpoint.smAndUp, 'mt-8': true }"
        :to="{ name: 'CanteensHome' }"
        width="fit-content"
      >
        Découvrir le réseau de cantines
      </v-btn>
      <v-btn v-if="loggedUser" x-large class="primary mt-8" :to="{ name: 'ManagementPage' }" width="fit-content">
        Accéder à mes cantines
      </v-btn>
      <v-btn v-else x-large class="primary mt-8" href="/creer-mon-compte" width="fit-content">
        Créer un compte gestionnaire
      </v-btn>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "PresentationBlock",
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>
