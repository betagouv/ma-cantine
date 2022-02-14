<template>
  <div>
    <v-row class="text-left">
      <v-spacer></v-spacer>
      <v-col cols="12" md="4">
        <v-card elevation="0" class="fill-height pa-4 d-flex flex-column">
          <v-img
            src="/static/images/elue.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="130"
          ></v-img>
          <v-card-title>
            <h2 class="text-h6 font-weight-bold">
              Je suis élu ou élue d'une collectivité
            </h2>
          </v-card-title>
          <v-card-text>
            Je veux savoir où en sont les établissements de ma région ou département sur leurs achats de produits bio,
            de qualité; comprendre leurs enjeux, leurs succès et difficultés.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="pa-4">
            <v-btn :to="{ name: 'PublicCanteenStatisticsPage' }" outlined color="primary">
              Accéder au tableau de bord
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card elevation="0" class="fill-height pa-4 d-flex flex-column">
          <v-img
            src="/static/images/ChartDoodle.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="130"
          ></v-img>
          <v-card-title>
            <h2 class="text-h6 font-weight-bold">
              Je suis gestionnaire d’un restaurant collectif
            </h2>
          </v-card-title>
          <v-card-text>
            Je veux être outillé sur les mesures à prendre en termes d’approvisionnement, savoir où je me situe par
            rapport aux objectifs des lois EGAlim et Climat, valoriser les initiatives mises en place.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="pa-4">
            <v-btn v-if="loggedUser" :to="{ name: 'ManagementPage' }" outlined color="primary">
              Gérer mes cantines
            </v-btn>
            <v-btn v-else href="/s-identifier" outlined color="primary">
              Me créer un compte / Me connecter
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card elevation="0" class="fill-height pa-0 pa-sm-4 d-flex flex-column">
          <v-img
            src="/static/images/parent.png"
            v-if="$vuetify.breakpoint.smAndUp"
            class="mx-auto rounded-0"
            contain
            max-height="130"
          ></v-img>
          <v-card-title class="text-h6 font-weight-bold">
            <h2 class="text-h6 font-weight-bold">Je suis convive et parent de convive</h2>
          </v-card-title>
          <v-card-text>
            Je veux savoir ce qu’il y a dans mon assiette dans mon restaurant d’entreprise; mais aussi ce que mange mon
            fils au collège et pouvoir interargir avec les gérant.e.s de l’EHPAD où sont logés mes parents.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="pa-4">
            <v-btn :to="{ name: 'CanteensHome' }" outlined color="primary">
              Rechercher parmi le réseau ma-cantine
            </v-btn>
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
