<template>
  <div>
    <v-card elevation="0" class="text-center text-md-right">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="150px" contain src="/static/images/doodles-dsfr/primary/SittingChef.png"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="12" md="7">
          <v-card-title>
            <v-spacer></v-spacer>
            <h1 class="text-h1">
              Mieux manger
              <br v-if="$vuetify.breakpoint.mdAndUp" />
              de la crèche à l’EHPAD
            </h1>
            <v-spacer v-if="$vuetify.breakpoint.smAndDown"></v-spacer>
          </v-card-title>
        </v-col>
        <v-col cols="3" class="d-flex flex-column" v-if="$vuetify.breakpoint.mdAndUp">
          <v-spacer></v-spacer>
          <v-img max-height="200px" contain src="/static/images/doodles-dsfr/primary/SittingChef.png"></v-img>
          <v-spacer></v-spacer>
        </v-col>
        <v-spacer v-if="$vuetify.breakpoint.mdAndUp"></v-spacer>
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
