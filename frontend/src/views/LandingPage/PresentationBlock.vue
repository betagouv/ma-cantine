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
          <v-card-title>
            <v-spacer></v-spacer>
            <h1 class="font-weight-black text-h4">
              Mieux manger
              <br v-if="$vuetify.breakpoint.mdAndUp" />
              de la crêche à l’EHPAD
            </h1>
            <v-spacer v-if="$vuetify.breakpoint.smAndDown"></v-spacer>
          </v-card-title>
          <v-card-text class="body-1">
            <p class="my-2">
              <span class="font-weight-bold">Accompagner la transition</span>
              de la restauration collective
            </p>
            <p class="my-2">
              <span class="font-weight-bold">Connaître les initiatives</span>
              prises par nos cantines
            </p>
            <p class="my-2">
              <span class="font-weight-bold">Suivre l'implémentation</span>
              de la loi EGAlim
            </p>
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
