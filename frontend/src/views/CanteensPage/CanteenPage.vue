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

      <p class="px-0 font-weight-black text-h6 grey--text text--darken-4 mt-4">
        Que mange-t-on dans les assiettes ?
      </p>
      <v-row>
        <v-col cols="12" sm="6" md="4">
          <v-card class="fill-height text-center pa-4 d-flex flex-column justify-center" outlined>
            <div class="grey--text text-h5 font-weight-black text--darken-2">
              25%
            </div>
            <div class="caption grey--text text--darken-2">
              Bio (2020)
            </div>
            <div class="mt-2">
              <v-img
                contain
                src="/static/images/quality-labels/logo_bio_eurofeuille.png"
                alt="Logo Agriculture Biologique"
                title="Logo Agriculture Biologique"
                max-height="35"
              />
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-card class="fill-height text-center d-flex flex-column justify-center" outlined>
            <div class="grey--text text-h5 font-weight-black text--darken-2">
              31%
            </div>
            <div class="caption grey--text text--darken-2">
              Durables et de qualité (2020)
            </div>
            <div class="d-flex mt-2 justify-center">
              <v-img
                contain
                v-for="label in labels"
                :key="label.title"
                :src="`/static/images/quality-labels/${label.src}`"
                :alt="label.title"
                :title="label.title"
                class="px-1"
                max-height="40"
                max-width="40"
              />
            </div>
          </v-card>
        </v-col>
      </v-row>

      <p class="px-0 font-weight-black text-h6 grey--text text--darken-4 mb-n4 mt-8">
        Nos démarches
      </p>
      <v-row class="mt-6">
        <v-col cols="12" v-for="(badge, key) in badges" :key="key">
          <v-card class="fill-height" elevation="0">
            <div class="d-flex align-start">
              <v-img width="30" max-width="35" contain :src="`/static/images/badge-${key}-2.png`"></v-img>
              <div>
                <v-card-title class="py-0 text-body-2 font-weight-bold">{{ badge.title }}</v-card-title>
                <v-card-subtitle class="pt-4" v-text="badge.subtitle"></v-card-subtitle>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <!-- <CanteenDashboard :diagnostics="diagnostics" :canteen="canteen" /> -->

      <v-divider class="my-8"></v-divider>

      <ContactForm id="contact" :canteen="canteen" />
    </div>
    <v-progress-circular indeterminate v-else style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
  </div>
</template>

<script>
import Constants from "@/constants"
// import CanteenDashboard from "@/components/CanteenDashboard"
import ContactForm from "./ContactForm"
import CanteenIndicators from "@/components/CanteenIndicators"
import labels from "@/data/quality-labels.json"

export default {
  data() {
    return {
      canteen: undefined,
      labels,
      badges: {
        appro: {
          title: "Des produits durables et de qualité",
          subtitle:
            "Ce qui est servi dans les assiettes est au moins à 20% bio et à 30% de produits durables et de qualité.",
        },
        waste: {
          title: "Vers du 0 gaspi alimentaire",
          subtitle: "La cantine est engagée dans une démarche de réduction drastique de son gaspillage.",
        },
        plastic: {
          title: "Une démarche 0 plastique",
          subtitle: "La cantine n’utilise plus du tout de plastique ni pour sa production ni pour le service.",
        },
        diversification: {
          title: "Equilibre nutritionnel et menu végé",
          subtitle: "Les protéines des repas servis peuvent aussi être présents dans des plats végétariens.",
        },
        info: {
          title: "Transparence et communication",
          subtitle:
            "Votre gestionnaire communique et informe ses convives de toutes ses démarches pour du mieux manger !",
        },
      },
    }
  },
  components: {
    // CanteenDashboard,
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
