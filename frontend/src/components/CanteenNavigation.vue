<template>
  <nav aria-label="Options de gestion de ma cantine" v-if="canteen">
    <v-card outlined class="mt-4">
      <v-list nav class="text-left">
        <v-list-item-group>
          <v-list-item :ripple="false" :to="{ name: 'ManagementPage' }">
            <v-icon small class="mr-2">$arrow-left-line</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold grey--text text--darken-1">
              Mes cantines
            </v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'CanteenForm' }">
            <v-icon small class="mr-2">$restaurant-fill</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">{{ canteen.name }}</v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'SatelliteManagement' }" v-if="isCentralCuisine">
            <v-icon small class="mr-2">$community-fill</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Satellites</v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'DiagnosticList' }">
            <v-icon small class="mr-2">$draft-fill</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Diagnostics</v-list-item-title>
          </v-list-item>
          <div v-if="$vuetify.display.smAndUp" class="mt-n2">
            <v-list-item
              v-for="diagnostic in orderedDiagnostics"
              :key="`diagnostic-${diagnostic.id}`"
              :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
              class="mb-0"
            >
              <v-list-item-title class="text-body-2 font-weight-bold pl-6 d-flex align-center">
                {{ diagnostic.year }}&nbsp;
                <v-icon v-if="hasActiveTeledeclaration(diagnostic)" color="grey" small>
                  $checkbox-circle-fill
                </v-icon>
                <v-icon v-if="shouldTeledeclare(diagnostic)" small color="amber darken-3">mdi-alert</v-icon>
                <span v-if="shouldTeledeclare(diagnostic)" class="font-weight-medium caption">Télédéclarez-le</span>
              </v-list-item-title>
            </v-list-item>
          </div>
          <v-list-item :ripple="false" :to="{ name: 'DashboardPage' }" v-if="orderedDiagnostics.length">
            <v-icon small class="mr-2">$award-fill</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">
              Améliorer ma cantine
            </v-list-item-title>
          </v-list-item>
          <div v-if="isPublished || hasSite">
            <v-list-item :ripple="false" :to="{ name: 'PublicationForm' }">
              <v-icon small class="mr-2">mdi-bullhorn</v-icon>
              <v-list-item-title class="text-body-2 font-weight-bold">
                Publication
                <v-icon v-if="isPublished" color="grey" small>
                  $checkbox-circle-fill
                </v-icon>
              </v-list-item-title>
              <v-badge dot inline v-if="readyToPublish"></v-badge>
            </v-list-item>
            <v-list-item v-if="isCentralCuisine" :ripple="false" :to="{ name: 'PublishSatellites' }" class="mt-n2">
              <v-list-item-title class="text-body-2 font-weight-bold pl-6">
                Publier mes satellites
              </v-list-item-title>
            </v-list-item>
          </div>
          <v-list-item v-else :ripple="false" :to="{ name: 'PublishSatellites' }" class="mt-n2">
            <v-icon small class="mr-2">mdi-bullhorn</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">
              Publier mes satellites
            </v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'CanteenGeneratePoster' }">
            <v-icon small class="mr-2">$article-fill</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Générer mon affiche</v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'CanteenManagers' }">
            <v-icon small class="mr-2">$team-fill</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Gestionnaires</v-list-item-title>
          </v-list-item>
          <v-list-item :ripple="false" :to="{ name: 'CanteenDeletion' }" class="rounded-lg">
            <v-icon small class="mr-2">$delete-fill</v-icon>
            <v-list-item-title class="text-body-2 font-weight-bold">Supprimer</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
  </nav>
</template>

<script>
import { hasDiagnosticApproData, lastYear } from "@/utils"

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
        hasDiagnosticApproData(diagnostic)
      )
    },
    isCentralCuisine() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    isPublished() {
      return this.canteen.publicationStatus === "published"
    },
    hasSite() {
      return ["site", "site_cooked_elsewhere", "central_serving"].includes(this.canteen.productionType)
    },
  },
  methods: {
    hasActiveTeledeclaration(diagnostic) {
      return diagnostic.teledeclaration && diagnostic.teledeclaration.status === "SUBMITTED"
    },
    shouldTeledeclare(diagnostic) {
      if (!window.ENABLE_TELEDECLARATION) return false
      return (
        (!diagnostic.teledeclaration || diagnostic.teledeclaration.status == "CANCELLED") &&
        diagnostic.year === lastYear()
      )
    },
  },
}
</script>
