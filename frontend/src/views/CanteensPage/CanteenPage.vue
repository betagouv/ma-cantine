<template>
  <div class="text-left">
    <BackLink :to="canteensHomeBacklink" text="Voir la liste des cantines" />
    <div v-if="canteen" id="canteen-dashboard">
      <v-card elevation="0" class="pa-0 mt-4 mb-8 text-left">
        <v-row class="align-center">
          <v-col
            v-if="canteen.logo"
            class="mr-4 d-none d-sm-block"
            cols="4"
            sm="3"
            md="2"
            style="border-right: solid 1px #dfdfdf;"
          >
            <v-img class="rounded" :src="canteen.logo" contain></v-img>
          </v-col>
          <v-col>
            <v-card-title class="text-h4 font-weight-black pa-0">
              <h1 class="text-h4 font-weight-black">
                {{ canteen.name }}
              </h1>
            </v-card-title>
            <v-spacer></v-spacer>
            <v-card-subtitle v-if="canteen.dailyMealCount || canteen.city" class="pa-0 pt-4 d-flex">
              <v-img
                v-if="canteen.logo"
                max-width="100px"
                max-height="80px"
                class="mr-4 rounded d-sm-none"
                :src="canteen.logo"
                contain
              ></v-img>
              <div>
                <CanteenIndicators :canteen="canteen" class="grey--text text--darken-3" />
                <router-link to="#contact">
                  <v-icon small>mdi-email-outline</v-icon>
                  Contactez-nous
                </router-link>
              </div>
            </v-card-subtitle>
          </v-col>
        </v-row>
      </v-card>

      <CanteenPublication :canteen="canteen" />

      <v-divider class="my-8"></v-divider>

      <ContactForm id="contact" :canteen="canteen" />
    </div>
    <v-progress-circular indeterminate v-else style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
  </div>
</template>

<script>
import { diagnosticsMap } from "@/utils"
import CanteenPublication from "@/components/CanteenPublication"
import ContactForm from "./ContactForm"
import CanteenIndicators from "@/components/CanteenIndicators"
import BackLink from "@/components/BackLink"
import labels from "@/data/quality-labels.json"

export default {
  data() {
    return {
      canteen: undefined,
      labels,
      canteensHomeBacklink: { name: "CanteensHome" },
    }
  },
  components: {
    CanteenPublication,
    ContactForm,
    CanteenIndicators,
    BackLink,
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
      return diagnosticsMap(diagnostics)
    },
  },
  methods: {
    setCanteen(canteen) {
      this.canteen = canteen
      if (canteen) document.title = `${this.canteen.name} - ${this.$store.state.pageTitleSuffix}`
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
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      if (from.name == "CanteensHome") {
        // keep filter settings in URL params
        vm.canteensHomeBacklink = from
      }
    })
  },
}
</script>
