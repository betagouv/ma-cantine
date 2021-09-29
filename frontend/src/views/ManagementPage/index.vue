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
            <v-card-text class="font-weight-bold pt-0 text-center">Ajouter une cantine</v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
    <div class="my-12">
      <h2 class="mb-4 text-h5 font-weight-black">Mes diagnostics</h2>
      <DiagnosticIntroduction v-if="!hasDiagnostics" class="body-2"></DiagnosticIntroduction>
      <div class="mb-8 ml-n4">
        <v-btn text color="primary" :to="{ name: 'NewDiagnostic' }" v-if="canteens.length">
          <v-icon class="mr-2">mdi-plus</v-icon>
          Ajouter un diagnostic
        </v-btn>
        <v-btn text color="primary" :to="{ name: 'DiagnosticsImporter' }">
          <v-icon class="mr-2">mdi-file-upload-outline</v-icon>
          Importer plusieurs diagnostics
        </v-btn>
      </div>

      <div v-for="canteen in $store.state.userCanteens" :key="`diag-${canteen.id}`">
        <div v-if="canteen.diagnostics && canteen.diagnostics.length">
          <v-row>
            <v-col cols="12" v-for="diagnostic in sortedDiagnosticsForCanteen(canteen)" :key="diagnostic.id">
              <DiagnosticCard :diagnostic="diagnostic" :class="{ 'fill-height': $vuetify.breakpoint.mdAndUp }" />
            </v-col>
          </v-row>
          <v-divider class="my-8"></v-divider>
        </div>
      </div>
    </div>
    <div class="my-8">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
  </div>
</template>

<script>
import CanteenCard from "./CanteenCard"
import DiagnosticCard from "@/components/DiagnosticCard"
import DiagnosticIntroduction from "@/components/DiagnosticIntroduction"
import UserTools from "./UserTools"

export default {
  components: { CanteenCard, DiagnosticCard, DiagnosticIntroduction, UserTools },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    canteens() {
      return this.$store.state.userCanteens
    },
    hasDiagnostics() {
      return this.canteens.length && this.canteens.some((c) => !!c.diagnostics.length)
    },
  },
  methods: {
    sortedDiagnosticsForCanteen(canteen) {
      return [...canteen.diagnostics].sort((diag1, diag2) => diag2.year - diag1.year)
    },
  },
}
</script>
