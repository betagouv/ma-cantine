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
              <v-list-item-title class="text-body-2 font-weight-bold pl-6">{{ diagnostic.year }}</v-list-item-title>
            </v-list-item>
          </div>
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
  },
}
</script>
