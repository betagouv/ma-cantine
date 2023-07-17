<template>
  <v-row class="text-left">
    <v-spacer></v-spacer>
    <v-col cols="12" md="4">
      <v-hover>
        <v-card
          outlined
          :to="loggedUser ? { name: 'ManagementPage' } : undefined"
          :href="loggedUser ? undefined : '/s-identifier'"
          class="fill-height pa-4 d-flex flex-column hover-transition dsfr"
        >
          <v-img
            src="/static/images/doodles-dsfr/secondary/SprintingDoodle.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="100"
          ></v-img>
          <v-card-title>
            <h2 class="text-h6 font-weight-bold">
              Gérer ma cantine pour atteindre mes objectifs
            </h2>
          </v-card-title>
          <v-card-text>
            Être outillé pour atteindre les objectifs des lois EGAlim et Climat
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 pt-0">
            <v-spacer></v-spacer>
            <v-icon color="primary">$arrow-right-line</v-icon>
          </v-card-actions>
        </v-card>
      </v-hover>
    </v-col>
    <v-col cols="12" md="4" :style="{ 'border-right': $vuetify.breakpoint.mdAndUp ? 'dotted 4px #e5fbf0' : 'none' }">
      <v-hover>
        <v-card
          outlined
          :to="{ name: 'PublicCanteenStatisticsPage' }"
          class="fill-height pa-4 d-flex flex-column hover-transition dsfr"
        >
          <v-img
            src="/static/images/doodles-dsfr/secondary/SitReadingDoodle.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="100"
          ></v-img>
          <v-card-title>
            <h2 class="text-h6 font-weight-bold">
              Suivre l'évolution de ma collectivité
            </h2>
          </v-card-title>
          <v-card-text>
            Savoir où en sont les établissements de ma région ou mon département
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 pt-0">
            <v-spacer></v-spacer>
            <v-icon color="primary">$arrow-right-line</v-icon>
          </v-card-actions>
        </v-card>
      </v-hover>
    </v-col>
    <v-col cols="12" md="4">
      <v-hover>
        <v-card
          outlined
          :to="{ name: 'CanteensHome' }"
          class="fill-height pa-4 d-flex flex-column hover-transition dsfr"
        >
          <v-img
            src="/static/images/doodles-dsfr/secondary/DogDoodle.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="100"
          ></v-img>
          <v-card-title class="text-h6 font-weight-bold">
            <h2 class="text-h6 font-weight-bold">En savoir plus sur la cantine que je fréquente</h2>
          </v-card-title>
          <v-card-text>
            Connaître les initiatives de mon restaurant ou celui de mes enfants
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 pt-0">
            <v-spacer></v-spacer>
            <v-icon color="primary">$arrow-right-line</v-icon>
          </v-card-actions>
        </v-card>
      </v-hover>
    </v-col>
    <v-spacer></v-spacer>
  </v-row>
</template>

<script>
export default {
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>

<style scoped>
/* a copy of the transition applied by vuetify to v-cards */
.hover-transition {
  transition-delay: 0s;
  transition-duration: 0.4s;
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.25, 0.8, 0.25, 1);
}
</style>
