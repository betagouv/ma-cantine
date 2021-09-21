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

      <p class="grey--text text--darken-2">
        Pour l'année 2020, on a achété
        <span class="text-h2 font-weight-black primary--text mx-2">25 %</span>
        de produits bios, et
        <span class="text-h2 font-weight-black primary--text mx-2">31 %</span>
        de produits durables et de qualité en plus.
      </p>
      <v-list two-line class="my-4">
        <v-subheader>Nos démarches</v-subheader>
        <v-list-item v-for="(badge, key) in badges" :key="key" class="px-0">
          <v-list-item-avatar>
            <v-img :src="`/static/images/badge-${key}.png`"></v-img>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title v-text="badge.title" class="mb-2"></v-list-item-title>
            <v-list-item-subtitle v-text="badge.subtitle"></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <CanteenDashboard :diagnostics="diagnostics" :canteen="canteen" />

      <v-divider class="my-8"></v-divider>

      <ContactForm id="contact" :canteen="canteen" />
    </div>
    <v-progress-circular indeterminate v-else style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
  </div>
</template>

<script>
import Constants from "@/constants"
import CanteenDashboard from "@/components/CanteenDashboard"
import ContactForm from "./ContactForm"
import CanteenIndicators from "@/components/CanteenIndicators"

export default {
  data() {
    return {
      canteen: undefined,
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
    CanteenDashboard,
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
