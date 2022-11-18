<template>
  <div>
    <div class="text-left">
      <h1 class="font-weight-black text-h4 my-4">
        Vos cantines satellites
      </h1>
      <SatelliteTable :canteen="canteen" />
      <v-divider class="my-8"></v-divider>
      <AddSatellite ref="satelliteTable" :canteen="canteen" @satelliteAdded="fetchSatelliteTable" />
    </div>
  </div>
</template>

<script>
import SatelliteTable from "./SatelliteTable"
import AddSatellite from "./AddSatellite"

export default {
  name: "SatelliteManagement",
  components: { SatelliteTable, AddSatellite },
  props: {
    originalCanteen: Object,
  },
  computed: {
    canteen() {
      return this.originalCanteen
    },
  },
  methods: {
    fetchSatelliteTable() {
      // this.$refs.satelliteTable.fetchCurrentPage()
    },
  },
  created() {
    document.title = `Satellites - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
}
</script>
