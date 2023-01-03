<template>
  <div>
    <h1 class="font-weight-black text-h4 my-4">Publier mes satellites</h1>
    <p>
      « {{ originalCanteen.name }} » est une cuisine centrale sans lieu de consommation. La publication concerne
      <b>uniquement les lieux de restauration recevant des convives.</b>
    </p>
    <p>
      Vous pouvez
      <router-link :to="{ name: 'NewCanteen' }">ajouter une cantine satellite</router-link>
      ou indiquer que
      <router-link
        :to="{
          name: 'CanteenModification',
          params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(originalCanteen) },
        }"
      >
        votre cuisine centrale reçoit aussi des convives sur place.
      </router-link>
    </p>
    <div>
      <v-row v-if="pubLoading" class="green--text">
        <v-col cols="1" justify-self="center">
          <v-progress-circular indeterminate></v-progress-circular>
        </v-col>
        <v-col>
          <p>Publications en cours...</p>
        </v-col>
      </v-row>
      <p v-else-if="showMassPublication">
        Vous pouvez publier
        <span v-if="unpublishedSatellites.length > 1">{{ unpublishedSatellites.length }} satellites.</span>
        <span v-else>1 satellite.</span>
        <v-btn class="primary ml-2" @click="massPublication">
          <span v-if="unpublishedSatellites.length > 1">Publier {{ unpublishedSatellites.length }} satellites</span>
          <span v-else>Publier la satellite</span>
        </v-btn>
      </p>
    </div>
    <SatelliteTable
      ref="satelliteTable"
      :headers="satelliteTableHeaders"
      :includeSatelliteLink="true"
      :canteen="canteen"
      :params="satelliteTableParams"
      :satelliteAction="satelliteAction"
      @mountedAndFetched="mountedAndFetched"
      @paramsChanged="updateRoute"
      @satellitesLoaded="updateSatellitesCounts"
    />
    <p v-if="published">
      Précédemment vous aviez choisi de publier cette cantine. En tant que cuisine centrale, vous pouvez désormais
      retirer cette publication.
    </p>
    <v-sheet v-if="published" rounded color="grey lighten-4 pa-3 my-6" class="d-flex">
      <v-spacer></v-spacer>
      <v-btn x-large color="primary" @click="removeCanteenPublication">
        Retirer la publication
      </v-btn>
    </v-sheet>
  </div>
</template>

<script>
import SatelliteTable from "@/components/SatelliteTable"

export default {
  name: "CentralKitchenPublication",
  components: { SatelliteTable },
  props: {
    originalCanteen: {
      type: Object,
    },
  },
  data() {
    return {
      published: this.originalCanteen.publicationStatus !== "draft",
      satelliteTableHeaders: [
        { text: "Nom", value: "name" },
        { text: "SIRET", value: "siret" },
        { text: "Publiée ?", value: "publicationStatus" },
        { text: "", value: "userCanView", sortable: false },
      ],
      unpublishedSatellites: [],
      pubLoading: false,
      pubSuccesses: [],
    }
  },
  computed: {
    canteen() {
      return this.originalCanteen
    },
    satelliteTableParams() {
      return this.$route.query
    },
    showMassPublication() {
      return this.unpublishedSatellites?.length
    },
  },
  methods: {
    removeCanteenPublication() {
      console.log("TODO: refactor to be an emit")
    },
    fetchSatellites() {
      this.$refs.satelliteTable.fetchCurrentPage()
    },
    mountedAndFetched() {
      this.$watch("$route", this.fetchSatellites)
    },
    updateSatellitesCounts(data) {
      this.satelliteCount = data.total
      this.unpublishedSatellites = data.unpublishedSatellites
    },
    updateRoute(params, isDefaultUpdate) {
      if (isDefaultUpdate) {
        this.$router.replace({ query: params })
      } else {
        this.$router.push({ query: params })
      }
    },
    satelliteAction(satellite) {
      const isDraft = satellite.publicationStatus === "draft"
      const store = this.$store
      const that = this
      return {
        text: isDraft ? "Publier" : "Retirer la publication",
        action() {
          store
            .dispatch(isDraft ? "publishCanteen" : "unpublishCanteen", {
              id: satellite.id,
              // is payload necessary if comments not being changed?
              // should there be an option to change the comments or is that too many buttons?
              payload: satellite,
            })
            .then((response) => {
              satellite.publicationStatus = response.publicationStatus
              const title = isDraft ? "La cantine satellite est publiée" : "La cantine satellite n'est plus publiée"
              store.dispatch("notify", { title, status: "success" })
            })
            .catch((e) => store.dispatch("notifyServerError", e))
            .finally(() => that.fetchSatellites())
        },
      }
    },
    massPublication() {
      this.pubLoading = true
      this.$store
        .dispatch("submitMultiplePublications", { ids: this.unpublishedSatellites })
        .then((response) => {
          this.pubSuccesses = response.ids
          const title =
            this.pubSuccesses.length > 1
              ? `${this.pubSuccesses.length} cantines satellites publiées`
              : `${this.pubSuccesses.length} cantine satellite publiée`
          this.$store.dispatch("notify", {
            title,
            status: "success",
          })
          // assume for UX that no more unpublished, but double checks with fetchSatellites
          this.unpublishedSatellites = []
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
        // refresh actions
        .then(() => this.fetchSatellites())
        .finally(() => {
          this.pubLoading = false
        })
    },
  },
}
</script>
