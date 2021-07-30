<template>
  <div class="text-left">
    <div class="mt-4">
      <p class="my-2 text-body-1 font-weight-bold">
        Bienvenue {{ loggedUser.firstName }}
        <v-btn text class="text-decoration-underline text-caption mb-1" :to="{ name: 'AccountEditor' }">
          <v-icon class="mr-1" small>mdi-pencil</v-icon>
          Modifier mon profil
        </v-btn>
      </p>
    </div>
    <div class="mt-4">
      <h1 class="my-4 text-h5 font-weight-black">Mes cantines</h1>
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
      <h2 class="mb-0 text-h5 font-weight-black">Mes diagnostics</h2>
      <v-btn text color="primary" class="mt-2 mb-8 ml-n4" :to="{ name: 'NewDiagnostic' }">
        <v-icon class="mr-2">mdi-plus</v-icon>
        Ajouter un diagnostic
      </v-btn>
      <v-btn text color="primary" class="mt-2 mb-8" :to="{ name: 'DiagnosticsImporter' }">
        <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
        Importer plusieurs diagnostics
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
      <h2 class="text-h5 font-weight-black">Mes outils</h2>
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
