<template>
  <div id="canteen-dashboard">
    <v-card elevation="0" class="pa-0 my-8 text-left">
      <v-card-title class="text-h4 font-weight-black">
        {{ canteen.name }}
      </v-card-title>
      <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city">
        <div v-if="canteen.dailyMealCount">
          <v-icon small>mdi-silverware-fork-knife</v-icon>
          {{ canteen.dailyMealCount }} repas par jour
        </div>
        <div v-if="canteen.city">
          <v-icon small>mdi-compass</v-icon>
          {{ canteen.city }}
        </div>
      </v-card-subtitle>
      <v-card-text>
        <v-btn outlined color="primary" exact :to="{ name: 'CanteensHome' }">
          <v-icon small class="mr-2">mdi-arrow-left</v-icon>
          Voir la liste des cantines
        </v-btn>
      </v-card-text>
    </v-card>

    <CanteenDashboard :diagnostics="diagnostics" />
  </div>
</template>

<script>
import Constants from "@/constants"
import CanteenDashboard from "@/components/CanteenDashboard"

export default {
  components: {
    CanteenDashboard,
  },
  props: ["id"],
  created() {
    document.title = `${this.canteen.name} - ma-cantine.beta.gouv.fr`
  },
  computed: {
    canteen() {
      return this.$store.state.publishedCanteens.find((x) => x.id == this.id)
    },
    diagnostics() {
      const diagnosis = this.canteen.diagnosis
      return {
        previous:
          diagnosis.find((x) => x.year === 2019) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
        latest:
          diagnosis.find((x) => x.year === 2020) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
      }
    },
  },
}
</script>
