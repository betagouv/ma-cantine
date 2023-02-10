<template>
  <div>
    <div class="text-left">
      <h1 class="font-weight-black text-h4 my-4">
        Vos cantines satellites
      </h1>
      <p v-if="satelliteCount !== null">
        Cette cuisine centrale fournit des repas
        {{ satelliteCanteensCount > 1 ? `à ${satelliteCanteensCount} cantines` : "à une cantine" }}.
        <span v-if="satelliteCount === 0">
          Vous n'avez ajouté aucune cantine satellite.
        </span>
        <span v-else-if="satelliteCanteensCount !== satelliteCount">Vous en avez renseigné {{ satelliteCount }}.</span>
      </p>
      <SatelliteTable
        ref="satelliteTable"
        :canteen="canteen"
        :params="satelliteTableParams"
        @mountedAndFetched="mountedAndFetched"
        @paramsChanged="updateRoute"
        @satellitesLoaded="updateSatellitesCount"
      />
      <v-divider class="my-8"></v-divider>
      <AddSatellite :canteen="canteen" @satelliteAdded="fetchSatellites" />
    </div>
  </div>
</template>

<script>
import SatelliteTable from "@/components/SatelliteTable"
import AddSatellite from "./AddSatellite"

export default {
  name: "SatelliteManagement",
  components: { SatelliteTable, AddSatellite },
  props: {
    originalCanteen: Object,
  },
  data() {
    return {
      satelliteCount: null,
    }
  },
  computed: {
    canteen() {
      return this.originalCanteen
    },
    satelliteTableParams() {
      return this.$route.query
    },
    satelliteCanteensCount() {
      return this.originalCanteen.satelliteCanteensCount
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
      this.$emit("satellitesCounted", { total: this.satelliteCount })
    },
    updateRoute(params, isDefaultUpdate) {
      if (isDefaultUpdate) {
        this.$router.replace({ query: params })
      } else {
        this.$router.push({ query: params })
      }
    },
  },
  created() {
    document.title = `Satellites - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
}
</script>
