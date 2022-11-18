<template>
  <div>
    <div v-if="visibleSatellites">
      <p>
        Cette cuisine centrale fournit des repas
        {{ satelliteCanteensCount > 1 ? `à ${satelliteCanteensCount} cantines` : "à une cantine" }}.
        <span v-if="!visibleSatellites || visibleSatellites.length === 0">
          Vous n'avez ajouté aucune cantine satellite.
        </span>
        <span v-else-if="satelliteCanteensCount !== visibleSatellites.length">
          Vous en avez renseigné {{ satelliteCount }}.
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
                demander l'accès pour pouvoir voir et modifier les données de cette cantine.
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
    </div>
  </div>
</template>

<script>
import DsfrTextarea from "@/components/DsfrTextarea"
import { getObjectDiff } from "@/utils"

export default {
  name: "SatelliteTable",
  components: { DsfrTextarea },
  props: {
    canteen: Object,
  },
  data() {
    return {
      ĺoading: false,
      limit: 10,
      visibleSatellites: null,
      satelliteCount: null,
      satelliteCanteensCount: this.canteen.satelliteCanteensCount,
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
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
  },
  methods: {
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
      // TODO: show loading circle using this var
      this.loading = true
      const url = `/api/v1/canteens/${this.canteen.id}/satellites/?${this.getApiQueryParams()}`
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
