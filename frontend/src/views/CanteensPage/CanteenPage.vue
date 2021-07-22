<template>
  <div id="canteen-dashboard">
    <v-card elevation="0" class="pa-0 my-8 text-left">
      <v-card-title>
        <h1 class="text-h4 font-weight-black">{{ canteen.name }}</h1>
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
        <router-link to="#contact">
          <v-icon small>mdi-email-outline</v-icon>
          Contactez-nous
        </router-link>
      </v-card-subtitle>
      <v-card-text>
        <v-btn outlined color="primary" exact :to="{ name: 'CanteensHome' }">
          <v-icon small class="mr-2">mdi-arrow-left</v-icon>
          Voir la liste des cantines
        </v-btn>
      </v-card-text>
    </v-card>

    <CanteenDashboard :diagnostics="diagnostics" />

    <v-divider class="my-8"></v-divider>

    <ContactForm id="contact" :canteen="canteen" />
  </div>
</template>

<script>
import Constants from "@/constants"
import CanteenDashboard from "@/components/CanteenDashboard"
import ContactForm from "./ContactForm"

export default {
  components: {
    CanteenDashboard,
    ContactForm,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
  },
  created() {
    document.title = `${this.canteen.name} - ma-cantine.beta.gouv.fr`
  },
  computed: {
    canteen() {
      const previousIdVersion = this.canteenUrlComponent.indexOf("--") === -1
      if (previousIdVersion) return this.$store.state.publishedCanteens.find((x) => x.id == this.canteenUrlComponent)
      return this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)
    },
    diagnostics() {
      const diagnostics = this.canteen.diagnostics
      return {
        previous:
          diagnostics.find((x) => x.year === 2019) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
        latest:
          diagnostics.find((x) => x.year === 2020) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
        provisionalYear1:
          diagnostics.find((x) => x.year === 2021) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2021 }),
        provisionalYear2:
          diagnostics.find((x) => x.year === 2022) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2022 }),
      }
    },
  },
}
</script>
