<template>
  <div class="text-left">
    <router-link :to="{ name: 'CanteensHome' }" class="mt-2 grey--text text--darken-1 caption">
      <v-icon small class="mr-2">mdi-arrow-left</v-icon>
      Voir la liste des cantines
    </router-link>
    <div v-if="canteen" id="canteen-dashboard">
      <v-card elevation="0" class="pa-0 mt-4 mb-8 text-left">
        <v-row class="align-center">
          <v-col v-if="canteen.mainImage" cols="12" sm="3">
            <v-img class="rounded" :src="canteen.mainImage"></v-img>
          </v-col>
          <v-col>
            <v-card-title class="text-h4 font-weight-black">
              <h1 class="text-h4 font-weight-black">
                {{ canteen.name }}
              </h1>
            </v-card-title>
            <v-spacer></v-spacer>
            <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city">
              <CanteenIndicators :canteen="canteen" class="grey--text text--darken-3" />
              <router-link to="#contact">
                <v-icon small>mdi-email-outline</v-icon>
                Contactez-nous
              </router-link>
            </v-card-subtitle>
          </v-col>
        </v-row>
      </v-card>

      <CanteenPublication />

      <v-divider class="my-8"></v-divider>

      <ContactForm id="contact" :canteen="canteen" />
    </div>
    <v-progress-circular indeterminate v-else style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
  </div>
</template>

<script>
import Constants from "@/constants"
import CanteenPublication from "@/components/CanteenPublication"
import ContactForm from "./ContactForm"
import CanteenIndicators from "@/components/CanteenIndicators"
import labels from "@/data/quality-labels.json"

export default {
  data() {
    return {
      canteen: undefined,
      labels,
    }
  },
  components: {
    CanteenPublication,
    ContactForm,
    CanteenIndicators,
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
