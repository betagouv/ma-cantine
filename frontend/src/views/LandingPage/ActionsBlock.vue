<template>
  <div>
    <v-row class="text-left">
      <v-spacer></v-spacer>
      <v-col cols="12" md="4">
        <v-card hover :to="{ name: 'PublicCanteenStatisticsPage' }" class="fill-height pa-4 d-flex flex-column">
          <v-img
            src="/static/images/elue.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="100"
          ></v-img>
          <v-card-title>
            <h2 class="text-h6 font-weight-bold">
              Étudier l'évolution de mon territoire
            </h2>
          </v-card-title>
          <v-card-text>
            Savoir où en sont les établissements de ma région ou département
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 pt-0">
            <v-spacer></v-spacer>
            <v-icon color="primary">mdi-arrow-right</v-icon>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card
          hover
          :to="loggedUser ? { name: 'ManagementPage' } : undefined"
          :href="!loggedUser ? '/s-identifier' : undefined"
          class="fill-height pa-4 d-flex flex-column"
        >
          <v-img
            src="/static/images/ChartDoodle.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="100"
          ></v-img>
          <v-card-title>
            <h2 class="text-h6 font-weight-bold">
              Gérer ma cantine et mes objectifs
            </h2>
          </v-card-title>
          <v-card-text>
            Être outillé pour attendre les objectifs des lois EGAlim et Climat
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 pt-0">
            <v-spacer></v-spacer>
            <v-icon color="primary">mdi-arrow-right</v-icon>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card hover :to="{ name: 'CanteensHome' }" class="fill-height pa-0 pa-sm-4 d-flex flex-column">
          <v-img
            src="/static/images/parent.png"
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
            <v-icon color="primary">mdi-arrow-right</v-icon>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      calculatorModal: false,
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
  methods: {
    closeCalculatorModal() {
      this.$refs.modalContent.stopVideo()
      this.calculatorModal = false
    },
    stopVideo(modalIsOpened) {
      if (!modalIsOpened) this.$refs.modalContent.stopVideo()
    },
  },
}
</script>
