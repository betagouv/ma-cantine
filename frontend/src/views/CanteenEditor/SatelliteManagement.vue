<template>
  <div>
    <div class="text-left" v-if="visibleSatellites">
      <h1 class="font-weight-black text-h4 my-4">
        Vos cantines satellites
      </h1>
      <p>
        Cette cuisine centrale fournit des repas
        {{ satelliteCanteensCount > 1 ? `à ${satelliteCanteensCount} cantines` : "à une cantine" }}.
        <span v-if="!visibleSatellites || visibleSatellites.length === 0">
          Vous n'avez ajouté aucune cantine satellite.
        </span>
        <span v-else-if="satelliteCanteensCount !== visibleSatellites.length">
          Vous en avez renseigné {{ visibleSatellites.length }}.
        </span>
      </p>
      <v-data-table
        :options.sync="options"
        :server-items-length="satelliteCount || 0"
        :items="visibleSatellites"
        :headers="headers"
      >
        <template v-slot:top>
          <v-dialog v-model="joinDialog" max-width="800px">
            <v-card class="text-left">
              <v-card-title>Rejoindre l'équipe de « {{ restrictedSatellite.name }} »</v-card-title>
              <v-card-text>
                Vous n'êtes pas encore un membre de l'équipe de « {{ restrictedSatellite.name }} » alors vous devez
                demander l'accès pour pourvoir voir et modifier les données de cette cantine.
                <DsfrTextarea
                  v-model="messageJoinCanteen"
                  label="Message (optionnel)"
                  hide-details="auto"
                  rows="2"
                  class="mt-2 body-2"
                />
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions class="py-4 pl-6">
                <v-btn color="primary" @click="sendMgmtRequest">
                  <v-icon class="mr-2">mdi-key</v-icon>
                  Demander l'accès
                </v-btn>
                <v-btn outlined color="primary" @click="joinDialog = false">
                  Annuler
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </template>
        <template v-slot:[`item.userCanView`]="{ item }">
          <v-btn outlined color="primary" :to="satelliteLink(item)" @click="satelliteAction(item)">
            {{ item.userCanView ? "Mettre à jour" : "Rejoindre l'équipe" }}
            <span class="d-sr-only">{{ item.userCanView ? "" : "de" }} {{ item.name }}</span>
          </v-btn>
        </template>
        <template v-slot:[`no-data`]>
          Vous n'avez pas renseigné des satellites
        </template>
      </v-data-table>

      <v-divider class="my-8"></v-divider>
      <h2 class="mb-2 text-h6 font-weight-bold">
        Ajoutez une nouvelle cantine satellite
      </h2>
      <p class="text-body-2">
        Utilisez le formulaire en dessous pour ajouter des satellites un après l'autre. Sinon, utilisez notre
        <router-link :to="{ name: 'DiagnosticsImporter' }">outil d'import des cantines et diagnostics</router-link>
        si vous avez les données en format CSV.
      </p>
      <v-card outlined>
        <v-card-text>
          <v-form ref="form" v-model="formIsValid">
            <v-row>
              <v-col cols="12" md="8">
                <label class="body-2" for="satellite-siret">SIRET</label>
                <DsfrTextField
                  id="satellite-siret"
                  hide-details="auto"
                  validate-on-blur
                  v-model="satellite.siret"
                  :rules="[validators.length(14), validators.luhn]"
                />
                <p class="caption mt-1 ml-2">
                  Utilisez cet
                  <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
                    outil de recherche pour trouver le SIRET
                    <v-icon color="primary" small>mdi-open-in-new</v-icon>
                  </a>
                  de votre cantine.
                </p>
              </v-col>
              <v-col cols="12" md="4">
                <label class="body-2" for="meal-count">Couverts par jour</label>
                <DsfrTextField
                  id="meal-count"
                  hide-details="auto"
                  validate-on-blur
                  v-model="satellite.dailyMealCount"
                  prepend-icon="$restaurant-fill"
                />
              </v-col>
            </v-row>
            <v-row class="mt-n4">
              <v-col cols="12" md="5">
                <label class="body-2" for="satellite-name">Nom de la cantine</label>
                <DsfrTextField
                  id="satellite-name"
                  hide-details="auto"
                  validate-on-blur
                  v-model="satellite.name"
                  :rules="[validators.required]"
                />
              </v-col>
              <v-col cols="12" md="5">
                <label class="body-2" for="sectors">Secteurs d'activité</label>
                <DsfrSelect
                  id="sectors"
                  class="mt-2"
                  multiple
                  :items="sectors"
                  v-model="satellite.sectors"
                  item-text="name"
                  item-value="id"
                  hide-details
                />
              </v-col>
              <v-spacer></v-spacer>
              <v-col class="align-self-end">
                <v-btn @click="saveSatellite" color="primary darken-1" class="mt-1" x-large>
                  Ajouter
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
import validators from "@/validators"
import { sectorsSelectList, getObjectDiff } from "@/utils"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"
import DsfrSelect from "@/components/DsfrSelect"

export default {
  name: "SatelliteManagement",
  components: { DsfrTextField, DsfrTextarea, DsfrSelect },
  props: {
    originalCanteen: Object,
  },
  data() {
    return {
      ĺoading: false,
      satellite: {},
      formIsValid: true,
      limit: 10,
      visibleSatellites: null,
      satelliteCount: null,
      satelliteCanteensCount: this.originalCanteen.satelliteCanteensCount,
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
      },
      headers: [
        { text: "Nom", value: "name" },
        { text: "SIRET", value: "siret" },
        { text: "Couverts par jour", value: "dailyMealCount" },
        { text: "", value: "userCanView" },
      ],
      joinDialog: false,
      restrictedSatellite: {},
      user: this.$store.state.loggedUser,
      messageJoinCanteen: null,
    }
  },
  computed: {
    offset() {
      return (this.options.page - 1) * this.limit
    },
    validators() {
      return validators
    },
    canteen() {
      return this.originalCanteen
    },
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
    },
  },
  methods: {
    saveSatellite() {
      if (!this.$refs.form.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        window.scrollTo(0, 0)
        return
      }
      this.$store
        .dispatch("addSatellite", { id: this.canteen.id, payload: this.satellite })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Cantine satellite ajoutée",
            message: "Votre cantine satellite a bien été créée.",
            status: "success",
          })
          this.satellite = {}
        })
        .then(this.fetchCurrentPage)
        .catch((error) => {
          if (error.message) {
            this.$store.dispatch("notify", {
              title: error.message,
              status: "error",
            })
          } else {
            this.$store.dispatch("notifyServerError", error)
          }
        })
    },
    populateParametersFromRoute() {
      const page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
      let sortBy = []
      let sortDesc = []

      this.$route.query["trier-par"] &&
        this.$route.query["trier-par"].split(",").forEach((element) => {
          const isDesc = element[0] === "-"
          sortBy.push(isDesc ? element.slice(1) : element)
          sortDesc.push(isDesc)
        })

      const newOptions = { sortBy, sortDesc, page }
      const optionChanges = this.options ? getObjectDiff(this.options, newOptions) : newOptions
      if (Object.keys(optionChanges).length > 0) this.$set(this, "options", newOptions)
    },
    fetchCurrentPage() {
      this.loading = true
      const url = `/api/v1/canteens/${this.originalCanteen.id}/satellites/?${this.getApiQueryParams()}`
      return fetch(url)
        .then((response) => {
          if (response.status != 200) throw new Error()
          return response.json()
        })
        .then((response) => {
          this.satelliteCount = response.count
          this.visibleSatellites = response.results
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
        .finally(() => {
          this.loading = false
        })
    },
    getApiQueryParams() {
      let apiQueryParams = `limit=${this.limit}&offset=${this.offset}`
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) apiQueryParams += `&ordering=${orderingItems.join(",")}`
      return apiQueryParams
    },
    onRouteChange() {
      this.fetchCurrentPage()
    },
    onOptionsChange() {
      this.$router.push({ query: this.getUrlQueryParams() }).catch(() => {})
    },
    getUrlQueryParams() {
      let urlQueryParams = { page: this.options.page }
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) urlQueryParams["trier-par"] = orderingItems.join(",")
      return urlQueryParams
    },
    getOrderingItems() {
      let orderParams = []
      if (this.options.sortBy && this.options.sortBy.length > 0)
        for (let i = 0; i < this.options.sortBy.length; i++)
          orderParams.push(this.options.sortDesc[i] ? `-${this.options.sortBy[i]}` : this.options.sortBy[i])
      return orderParams
    },
    addWatchers() {
      this.$watch("options", this.onOptionsChange, { deep: true })
      this.$watch("$route", this.onRouteChange)
    },
    satelliteLink(satellite) {
      if (satellite.userCanView) {
        return {
          name: "CanteenModification",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(satellite) },
        }
      }
    },
    satelliteAction(satellite) {
      if (!satellite.userCanView) {
        this.restrictedSatellite = satellite
        this.joinDialog = true
      }
    },
    sendMgmtRequest() {
      const payload = {
        email: this.user.email,
        name: `${this.user.firstName} ${this.user.lastName}`,
        message: this.messageJoinCanteen,
      }

      this.$store
        .dispatch("sendCanteenTeamRequest", { canteenId: this.restrictedSatellite.id, payload })
        .then(() => {
          this.messageJoinCanteen = null
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé.`,
          })
          window.scrollTo(0, 0)
          this.joinDialog = false
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
  created() {
    document.title = `Satellites - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
  beforeMount() {
    if (!this.$route.query["page"]) this.$router.replace({ query: { page: 1 } })
  },
  mounted() {
    this.populateParametersFromRoute()
    if (this.hasActiveFilter) this.showFilters = true
    return this.fetchCurrentPage().then(this.addWatchers)
  },
}
</script>

<style scoped>
.v-data-table {
  border: solid 1px #ddd;
}

/* Hides items-per-row */
.v-data-table >>> .v-data-footer__select {
  visibility: hidden;
}
</style>
