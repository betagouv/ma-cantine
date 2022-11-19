<template>
  <div>
    <v-data-table
      :options.sync="options"
      :server-items-length="satelliteCount || 0"
      :items="visibleSatellites"
      :headers="headers"
      v-if="visibleSatellites"
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
        <v-btn v-if="!item.userCanView" outlined color="primary" @click="requestAccess(item)">
          Rejoindre l'équipe
          <span class="d-sr-only">de {{ item.name }}</span>
        </v-btn>
        <v-btn v-else-if="satelliteAction(item)" outlined color="primary" @click="satelliteAction(item).action()">
          {{ satelliteAction(item).text }}
          <span class="d-sr-only">{{ item.name }}</span>
        </v-btn>
        <v-btn v-else-if="satelliteLink(item)" outlined color="primary" :to="satelliteLink(item)">
          Mettre à jour
          <span class="d-sr-only">{{ item.name }}</span>
        </v-btn>
      </template>
      <template v-slot:[`no-data`]>
        Vous n'avez pas renseigné des satellites
      </template>
    </v-data-table>
  </div>
</template>

<script>
/*
When displaying paginated, filterable, sortable data, there are lots of things to keep in mind.
The URL needs to be updated with changes to page, filter or sort.
This URL needs to be in French, not English, so our data model fields need to be translated for the filter param options,
  and for the sort values.
The data needs to be reloaded on change to the parameters.
The correct data needs to be fetched when loading the URL directly.
We want to show a loading spinner when the data is being fetched.
Error handling if the data cannot be fetched.
We need to request the right results based on the page requested, determined by the offset and the limit.
Filter parameters have different parsing requirements based on data type and if the value is an array or not.
The URL structure of different paginated pages should be consistent
  e.g. do you pass params like `foo=bar&foo=baz` or `foo=bar,baz`?

For satellites in particular:
The manager of the central kitchen may not be a manager of the satellite.

Ideally, routes are managed by views, not components.
*/

import DsfrTextarea from "@/components/DsfrTextarea"
import { getObjectDiff } from "@/utils"

export default {
  name: "SatelliteTable",
  components: { DsfrTextarea },
  props: {
    canteen: Object,
    sortParam: {
      type: String,
      default: "trier-par",
    },
    params: {
      type: Object,
      default: () => ({}),
    },
    headers: {
      type: Array,
      default() {
        return [
          { text: "Nom", value: "name" },
          { text: "SIRET", value: "siret" },
          { text: "Couverts par jour", value: "dailyMealCount" },
          // TODO: shouldn't be able to sort on this, since there is no header text
          { text: "", value: "userCanView" },
        ]
      },
    },
    // this function should return an object with two keys:
    // action: a function that takes the satellite
    // text: to be displayed with the button
    satelliteAction: {
      type: Function,
      optional: true,
    },
  },
  data() {
    return {
      ĺoading: false,
      limit: 10,
      visibleSatellites: null,
      satelliteCount: null,
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
      },
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
  },
  methods: {
    populateOptionsFromParams() {
      const page = this.params.page ? parseInt(this.params.page) : 1
      let sortBy = []
      let sortDesc = []
      let urlSortBy = this.params[this.sortParam]
      if (!urlSortBy) urlSortBy = []
      else if (!Array.isArray(urlSortBy)) urlSortBy = [urlSortBy]

      urlSortBy.forEach((element) => {
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
          this.$emit("satellitesLoaded", { total: this.satelliteCount })
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
      this.$emit("paramsChanged", this.getUrlQueryParams())
    },
    getUrlQueryParams() {
      let urlQueryParams = { page: this.options.page }
      const orderingItems = this.getOrderingItems()
      if (orderingItems.length > 0) urlQueryParams[this.sortParam] = orderingItems.join(",")
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
    },
    satelliteLink(satellite) {
      if (satellite.userCanView) {
        return {
          name: "CanteenModification",
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(satellite) },
        }
      }
    },
    requestAccess(satellite) {
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
    if (!this.params["page"]) this.$emit("paramsChanged", { page: 1 }, true)
  },
  mounted() {
    this.populateOptionsFromParams()
    return this.fetchCurrentPage().then(() => {
      this.addWatchers()
      this.$emit("mountedAndFetched")
    })
  },
}
/*
Here is some suggested parent config to get you started with this component
template:
  <SatelliteTable
    ref="satelliteTable"
    :canteen="canteen"
    :params="satelliteTableParams"
    @mountedAndFetched="mountedAndFetched"
    @paramsChanged="updateRoute"
    @satellitesLoaded="updateSatellitesCount"
  />

script:
import SatelliteTable from "@/components/SatelliteTable"

  data() {
    return {
      satelliteCount: null,
    }
  },
  computed: {
    canteen() {
      return ...
    },
    satelliteTableParams() {
      return this.$route.query
    },
  },
  methods: {
    fetchSatellites() {
      this.$refs.satelliteTable.fetchCurrentPage()
    },
    mountedAndFetched() {
      this.$watch("$route", this.fetchSatellites)
    },
    updateSatellitesCount(data) {
      this.satelliteCount = data.total
    },
    updateRoute(params, isDefaultUpdate) {
      if (isDefaultUpdate) {
        this.$router.replace({ query: params })
      } else {
        this.$router.push({ query: params })
      }
    },
  },
*/
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
