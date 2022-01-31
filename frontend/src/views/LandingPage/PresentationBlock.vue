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
        <v-col cols="12" sm="9" md="5">
          <v-card-title class="pl-0">
            <h1 class="font-weight-black text-h4">Diagnostiquer ma cantine sur les mesures de la loi EGAlim</h1>
          </v-card-title>
          <v-card-text>
            La loi EGAlim vise à apporter une alimentation saine, de qualité et plus durable dans nos assiettes.
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
        Découvrir nos cantines
      </v-btn>
      <v-btn v-if="loggedUser" x-large class="primary mt-8" :to="{ name: 'ManagementPage' }" width="fit-content">
        Accéder à mes cantines
      </v-btn>
      <v-btn v-else x-large class="primary mt-8" href="/creer-mon-compte" width="fit-content">
        Créer mon compte
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
