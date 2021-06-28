<template>
  <div class="text-left">
    <div class="mt-8">
      <p class="my-4 text-h5 font-weight-black">
        Bienvenue {{ loggedUser.firstName }}
        <v-btn text class="text-decoration-underline" :to="{ name: 'AccountEditor' }">
          <v-icon class="mr-1" small>mdi-pencil</v-icon>
          Modifier mon profil
        </v-btn>
      </p>
    </div>
    <div class="mt-8">
      <p class="my-4 text-h5 font-weight-black">Mes cantines</p>
      <v-row>
        <v-col cols="12" sm="6" md="4" height="100%" v-for="canteen in canteens" :key="`canteen-${canteen.id}`">
          <CanteenCard :canteen="canteen" class="fill-height" />
        </v-col>
        <v-col cols="12" sm="6" md="4" height="100%">
          <v-card
            color="grey lighten-5"
            class="fill-height d-flex flex-column align-center justify-center"
            min-height="280"
            :to="{ name: 'NewCanteen' }"
          >
            <v-icon size="100">mdi-plus</v-icon>
            <v-card-text class="font-weight-bold pt-0 text-center">
              Ajouter une cantine
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div class="my-12">
      <p class="mb-0 text-h5 font-weight-black">Mes diagnostics</p>
      <v-btn text color="primary" class="mt-2 mb-8 ml-n4" :to="{ name: 'NewDiagnostic' }">
        <v-icon class="mr-2">mdi-plus</v-icon>
        Ajouter un diagnostic
      </v-btn>

      <div v-for="canteen in $store.state.userCanteens" :key="`diag-${canteen.id}`">
        <v-row>
          <v-col cols="12" v-for="diagnostic in sortedDiagnosticsForCanteen(canteen)" :key="diagnostic.id">
            <DiagnosticCard :diagnostic="diagnostic" :class="{ 'fill-height': $vuetify.breakpoint.mdAndUp }" />
          </v-col>
        </v-row>
        <v-divider v-if="canteen.diagnostics && canteen.diagnostics.length" class="my-8"></v-divider>
      </div>
    </div>
    <div class="my-8">
      <p class="text-h5 font-weight-black">Mes outils</p>
      <UserTools />
    </div>
  </div>
</template>

<script>
import CanteenCard from "./CanteenCard"
import DiagnosticCard from "@/components/DiagnosticCard"
import UserTools from "./UserTools"

export default {
  components: { CanteenCard, DiagnosticCard, UserTools },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    canteens() {
      return this.$store.state.userCanteens
    },
  },
  methods: {
    sortedDiagnosticsForCanteen(canteen) {
      return [...canteen.diagnostics].sort((diag1, diag2) => diag2.year - diag1.year)
    },
  },
}
</script>
