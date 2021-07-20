<template>
  <div>
    <div v-if="canteen" id="canteen-dashboard">
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
    <v-progress-circular indeterminate v-else style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
  </div>
</template>

<script>
import Constants from "@/constants"
import CanteenDashboard from "@/components/CanteenDashboard"

export default {
  data() {
    return {
      canteen: undefined,
    }
  },
  components: {
    CanteenDashboard,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
  },
  computed: {
    diagnostics() {
      if (!this.canteen) return
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
  methods: {
    setCanteen(canteen) {
      this.canteen = canteen
      if (canteen) document.title = `${this.canteen.name} - ma-cantine.beta.gouv.fr`
    },
  },
  beforeMount() {
    const previousIdVersion = this.canteenUrlComponent.indexOf("--") === -1
    const existingCanteens = this.$store.state.publishedCanteens.flatMap((x) => x.results)
    let canteen = previousIdVersion
      ? existingCanteens.find((x) => x.id == this.canteenUrlComponent)
      : this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)

    if (canteen) return this.setCanteen(canteen)

    const id = previousIdVersion ? this.canteenUrlComponent : this.canteenUrlComponent.split("--")[0]
    return fetch(`/api/v1/publishedCanteens/${id}`)
      .then((response) => {
        if (response.status != 200) throw new Error()
        response.json().then(this.setCanteen)
      })
      .catch(() => {
        this.$store.dispatch("notify", {
          message: "Nous n'avons pas trouvé cette cantine",
          status: "error",
        })
        this.$router.push({ name: "CanteensHome" })
      })
  },
}
</script>
