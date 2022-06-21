<template>
  <nav aria-label="Options de gestion de ma cantine" v-if="canteen">
    <v-card outlined class="mt-4">
      <v-list nav class="text-left">
        <v-list-item-group>
          <v-list-item :ripple="false" :to="{ name: 'ManagementPage' }">
            <v-icon small class="mr-2">mdi-arrow-left</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold grey--text text--darken-1">
              Mes cantines
            </v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'CanteenForm' }">
            <v-icon small class="mr-2">mdi-silverware-fork-knife</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">{{ canteen.name }}</v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'DiagnosticList' }">
            <v-icon small class="mr-2">mdi-format-list-checks</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Diagnostics</v-list-item-title>
          </v-list-item>
          <div v-if="$vuetify.breakpoint.smAndUp">
            <v-list-item
              v-for="diagnostic in orderedDiagnostics"
              :key="`diagnostic-${diagnostic.id}`"
              :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
              class="mb-0"
            >
              <v-list-item-title class="text-body-2 font-weight-bold pl-6">
                {{ diagnostic.year }}
                <v-icon v-if="hasActiveTeledeclaration(diagnostic)" color="grey" small class="mt-n1 ml-1">
                  mdi-check-circle
                </v-icon>
              </v-list-item-title>
            </v-list-item>
          </div>
          <v-list-item :ripple="false" :to="{ name: 'DashboardPage' }" v-if="orderedDiagnostics.length">
            <v-icon small class="mr-2">mdi-star-shooting</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">
              Améliorer ma cantine
            </v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'PublicationForm' }">
            <v-icon small class="mr-2">mdi-bullhorn</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">
              Publication
            </v-list-item-title>
            <v-badge dot inline v-if="readyToPublish"></v-badge>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'CanteenManagers' }">
            <v-icon small class="mr-2">mdi-account-group</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Gestionnaires</v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'CanteenDeletion' }" class="rounded-lg">
            <v-icon small class="mr-2">mdi-trash-can</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Supprimer</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
  </nav>
</template>

<script>
import { isDiagnosticComplete, lastYear } from "@/utils"

export default {
  name: "CanteenNavigation",
  props: ["canteen"],
  computed: {
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    orderedDiagnostics() {
      return [...this.canteen.diagnostics].sort((a, b) => (a.year > b.year ? -1 : 1))
    },
    readyToPublish() {
      const diagnostic = this.canteen.diagnostics.find((x) => x.year === lastYear())
      return (
        this.canteen.productionType !== "central" &&
        this.canteen.publicationStatus === "draft" &&
        !!diagnostic &&
        isDiagnosticComplete(diagnostic)
      )
    },
  },
  methods: {
    hasActiveTeledeclaration(diagnostic) {
      return diagnostic.teledeclaration && diagnostic.teledeclaration.status === "SUBMITTED"
    },
  },
}
</script>
